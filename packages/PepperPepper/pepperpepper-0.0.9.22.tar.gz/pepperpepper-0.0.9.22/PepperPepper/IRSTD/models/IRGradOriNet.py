from PepperPepper.layers import IRGradOri, MultiScaleSPWDilate, AttentionalCS, Coopetition_Fuse, ResidualLeakBlock, AlternateCat, IRFourierStatFocus
from torch.nn.init  import trunc_normal_
import torch
import torch.nn as nn
import torch.nn.functional as F
from thop import profile






class IRGradSkip(nn.Module):
    def __init__(self, dim, kernel_size=5):
        super().__init__()
        self.dim = dim
        self.kernel_size = kernel_size

        self.gradori = IRGradOri(dim, kernel_size=kernel_size)
        self.proj = nn.Sequential(
            nn.Conv2d(dim * 2, dim, kernel_size=1),
            nn.BatchNorm2d(dim),
            nn.LeakyReLU(0.2),
        )
        self.MSPWD = MultiScaleSPWDilate(dim)
        self.ACS = AttentionalCS(dim)
        self.ACT = AlternateCat(dim=1)


    def forward(self, x):
        gradori = self.gradori(x)
        act = self.ACT(gradori, x)
        fproj = self.proj(act)
        fmspwd = self.MSPWD(fproj)
        fout = self.ACS(fmspwd)
        return fout



class Uplayer(nn.Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.proj = nn.Conv2d(in_channels, out_channels, 1)
        self.CPF = Coopetition_Fuse(2)
        self.residual = ResidualLeakBlock(out_channels, out_channels)

    def forward(self, x, skip_x):
        fproj = self.proj(x)
        assert fproj.shape == skip_x.shape
        fcpf = self.CPF([fproj, skip_x])
        cout = self.residual(fcpf)
        return cout



class Downlayer(nn.Module):
    def __init__(self, in_channels, out_channels, stride = 1):
        super().__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.stride = stride

        self.step1 = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, 1),
            nn.BatchNorm2d(out_channels),
            nn.LeakyReLU(0.2, inplace=True)
        )

        self.step2 = nn.Sequential(
            nn.Conv2d(out_channels, out_channels, 3, 1, 1),
            nn.BatchNorm2d(out_channels)
        )

        self.irfs = IRFourierStatFocus(out_channels, out_channels)


        if stride != 1 or out_channels != in_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=stride),
                nn.BatchNorm2d(out_channels),
            )
        else:
            self.shortcut = None

        self.relu = nn.LeakyReLU(0.2, inplace=True)

    def forward(self, x):
        residual = x
        f1 = self.step1(x)
        irfse = self.irfs(f1)
        f2 = self.step2(f1)


        if self.shortcut is not None:
            residual = self.shortcut(residual)

        out = self.relu(residual + f2 + irfse)


        return out




class IRGradOriNet(nn.Module):
    def __init__(self, in_dim = 3, dim=16, num_classes=1):
        super().__init__()
        self.title = 'IRGradOriNet_IRFS_IRGSV2'
        self.in_dim = in_dim
        self.dim = dim
        self.num_classes = num_classes

        self.downsample = nn.MaxPool2d(2, 2)
        self.upsample = nn.Upsample(scale_factor=2)

        self.downlayer1 = Downlayer(in_channels=in_dim, out_channels=dim * 1)
        self.downlayer2 = Downlayer(in_channels=dim * 1 , out_channels=dim * 2)
        self.downlayer3 = Downlayer(in_channels=dim * 2, out_channels=dim * 4)
        self.downlayer4 = Downlayer(in_channels=dim * 4, out_channels=dim * 8)
        self.downlayer5 = Downlayer(in_channels=dim * 8, out_channels=dim * 16)

        self.skip1 = IRGradSkip(dim=dim, kernel_size=5)
        self.skip2 = IRGradSkip(dim=dim * 2, kernel_size=5)
        self.skip3 = IRGradSkip(dim=dim * 4, kernel_size=5)
        self.skip4 = IRGradSkip(dim=dim * 8, kernel_size=5)
        # self.skip5 = IRGradSkip(dim=dim * 16, kernel_size=5)

        self.uplayer4 = Uplayer(in_channels=dim * 16, out_channels=dim * 8)
        self.uplayer3 = Uplayer(in_channels=dim * 8, out_channels=dim * 4)
        self.uplayer2 = Uplayer(in_channels=dim * 4, out_channels=dim * 2)
        self.uplayer1 = Uplayer(in_channels=dim * 2, out_channels=dim * 1)

        self.cout = nn.Conv2d(dim, num_classes, 1)
        self.apply(self._init_weights)



    def forward(self, x):
        if x.size(1) == 1:
            x = x.repeat(1, self.in_dim, 1, 1)

        f1 = self.downlayer1(x)
        f2 = self.downlayer2(self.downsample(f1))
        f3 = self.downlayer3(self.downsample(f2))
        f4 = self.downlayer4(self.downsample(f3))
        f5 = self.downlayer5(self.downsample(f4))

        fskip1 = self.skip1(f1)
        fskip2 = self.skip2(f2)
        fskip3 = self.skip3(f3)
        fskip4 = self.skip4(f4)
        # fskip5 = self.skip5(f5)

        d4 = self.uplayer4(self.upsample(f5), fskip4)
        d3 = self.uplayer3(self.upsample(d4), fskip3)
        d2 = self.uplayer2(self.upsample(d3), fskip2)
        d1 = self.uplayer1(self.upsample(d2), fskip1)
        out = self.cout(d1)

        return out

    def _init_weights(self, m):
        """ 增强版权重初始化方法，支持主流网络层类型
        核心策略：
        - Transformer风格线性层初始化
        - CNN优化卷积层初始化
        - 自适应归一化层处理
        """

        # 线性层初始化（适配Transformer结构）
        if isinstance(m, nn.Linear):
            trunc_normal_(m.weight, std=0.02)  # 截断正态分布，限制极端值
            if m.bias is not None:  # 偏置项零初始化
                nn.init.zeros_(m.bias)

                # 卷积层初始化（适配CNN结构）
        elif isinstance(m, nn.Conv2d):
            # 计算Kaiming初始化标准差
            fan_in = m.kernel_size[0] * m.kernel_size[1] * m.in_channels
            # 使用ReLU激活的推荐模式（兼容GELU/SiLU）
            nn.init.kaiming_normal_(m.weight,
                                    mode='fan_in',
                                    nonlinearity='relu')
            if m.bias is not None:  # 偏置项零初始化
                nn.init.zeros_(m.bias)

                # 归一化层初始化
        elif isinstance(m, (nn.LayerNorm, nn.BatchNorm2d)):
            nn.init.ones_(m.weight)  # 缩放系数初始为1
            nn.init.zeros_(m.bias)  # 平移系数初始为0



if __name__ == '__main__':
    model = IRGradOriNet().cuda()
    inputs = torch.rand(1, 1, 256, 256).cuda()
    output = model(inputs)
    # print(output)
    if torch.isnan(output).any():
        print(f"NaN detected at layer output: {output}")
        # break

    flops, params = profile(model, (inputs,))

    print("-" * 50)
    print('FLOPs = ' + str(flops / 1000 ** 3) + ' G')
    print('Params = ' + str(params / 1000 ** 2) + ' M')


