from PepperPepper.environment import torch, nn, einops, rearrange, Rearrange

class SpatialAttention(nn.Module):
    """增强目标空间位置的注意力机制"""
    def __init__(self, kernel_size=7):
        super().__init__()
        assert kernel_size % 2 == 1, "Kernel size must be odd"

        self.conv = nn.Conv2d(2, 1, kernel_size, padding=kernel_size // 2)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        # 空间维度统计
        avg_out = torch.mean(x,  dim=1, keepdim=True)
        max_out, _ = torch.max(x,  dim=1, keepdim=True)


        # 空间特征拼接
        spatial_features = torch.cat([avg_out,  max_out], dim=1)
        spatial_weights = self.sigmoid(self.conv(spatial_features))
        return x * spatial_weights.expand_as(x)


class ChannelAttention(nn.Module):
    """增强目标相关通道特征的注意力机制"""

    def __init__(self, in_channels, reduction_ratio=2):
        super().__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.max_pool = nn.AdaptiveMaxPool2d(1)

        # 双路径注意力机制
        self.shared_mlp = nn.Sequential(
            nn.Linear(in_channels, in_channels // reduction_ratio),
            nn.ReLU(inplace=True),
            nn.Linear(in_channels // reduction_ratio, in_channels)
        )

        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        # 通道维度统计
        avg_out = self.shared_mlp(self.avg_pool(x).view(x.size(0), -1))
        max_out = self.shared_mlp(self.max_pool(x).view(x.size(0), -1))

        # 注意力权重融合
        channel_weights = self.sigmoid(avg_out + max_out).unsqueeze(2).unsqueeze(3)
        return x * channel_weights.expand_as(x)


class AttentionalCS(nn.Module):
    """完整注意力调制模块（通道+空间级联）"""

    def __init__(self, dim):
        super().__init__()
        self.ca = ChannelAttention(dim)
        self.sa = SpatialAttention()

    def forward(self, x):
        x = self.ca(x)  # 先增强通道维度
        x = self.sa(x)  # 再增强空间维度
        return x



class PixelAttention(nn.Module):
    def __init__(self, dim):
        super(PixelAttention, self).__init__()
        self.pa2 = nn.Conv2d(2 * dim, dim, 7, padding=3, padding_mode='reflect', groups=dim, bias=True)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x, pattn1):
        B, C, H, W = x.shape
        x = x.unsqueeze(dim=2)  # B, C, 1, H, W
        pattn1 = pattn1.unsqueeze(dim=2)  # B, C, 1, H, W
        x2 = torch.cat([x, pattn1], dim=2)  # B, C, 2, H, W
        x2 = Rearrange('b c t h w -> b (c t) h w')(x2)
        pattn2 = self.pa2(x2)
        pattn2 = self.sigmoid(pattn2)
        return pattn2



# sobel注意力机制
class SobelAttention(torch.nn.Module):
    def __init__(self, in_channels):
        super(SobelAttention, self).__init__()
        self.channels = in_channels

        # sobel算子
        self.sobel_v = torch.nn.Conv2d(in_channels=in_channels, out_channels=in_channels, kernel_size=3, padding=1,
                                       bias=False)
        self.sobel_h = torch.nn.Conv2d(in_channels=in_channels, out_channels=in_channels, kernel_size=3, padding=1,
                                       bias=False)

        # 初始化卷积核
        sobel_kernel_v = torch.tensor([[0, -1, 0],
                                       [0, 0, 0],
                                       [0, 1, 0]], dtype=torch.float32).view(1, 1, 3, 3)
        sobel_kernel_h = torch.tensor([[0, 0, 0],
                                       [-1, 0, 1],
                                       [0, 0, 0]], dtype=torch.float32).view(1, 1, 3, 3)

        # 将卷积核扩展到多个通道
        sobel_kernel_v = sobel_kernel_v.repeat(in_channels, in_channels, 1, 1)
        sobel_kernel_h = sobel_kernel_h.repeat(in_channels, in_channels, 1, 1)

        self.sobel_v.weight = torch.nn.Parameter(sobel_kernel_v, requires_grad=False)
        self.sobel_h.weight = torch.nn.Parameter(sobel_kernel_h, requires_grad=False)



        # sobel算子
        self.sobel3_x = torch.nn.Conv2d(in_channels=in_channels, out_channels=in_channels, kernel_size=3, padding=1, bias=False, padding_mode='reflect')
        self.sobel3_y = torch.nn.Conv2d(in_channels=in_channels, out_channels=in_channels, kernel_size=3, padding=1, bias=False, padding_mode='reflect')
        self.sobel5_x = torch.nn.Conv2d(in_channels=in_channels, out_channels=in_channels, kernel_size=5, padding=2, bias=False, padding_mode='reflect')
        self.sobel5_y = torch.nn.Conv2d(in_channels=in_channels, out_channels=in_channels, kernel_size=5, padding=2, bias=False, padding_mode='reflect')
        self.sobel7_x = torch.nn.Conv2d(in_channels=in_channels, out_channels=in_channels, kernel_size=7, padding=3, bias=False, padding_mode='reflect')
        self.sobel7_y = torch.nn.Conv2d(in_channels=in_channels, out_channels=in_channels, kernel_size=7, padding=3, bias=False, padding_mode='reflect')

        # 初始化卷积核
        sobel_kernel3_x = torch.tensor([[1, 0, -1],
                                       [2, 0, -2],
                                       [1, 0, -1]], dtype=torch.float32).view(1, 1, 3, 3)
        sobel_kernel3_y = torch.tensor([[1, 2, 1],
                                       [0, 0, 0],
                                       [-1, -2, -1]], dtype=torch.float32).view(1, 1, 3, 3)

        sobel_kernel5_x = torch.tensor(
            [[-2, -1, 0, 1, 2],
             [-4, -3, 0, 3, 4],
             [-6, -5, 0, 5, 6],
             [-4, -3, 0, 3, 4],
             [-2, -1, 0, 1, 2]], dtype=torch.float32
        ).view(1,1,5,5)

        sobel_kernel5_y = torch.tensor(
            [[2, 4, 6, 4, 2],
             [1, 3, 5, 3, 1],
             [0, 0, 0, 0, 0],
             [-1, -3, -5, -3, -1],
             [-2, -4, -6, -4, -2]], dtype=torch.float32
        ).view(1,1,5,5)

        sobel_kernel7_x = torch.tensor(
            [[-3, -2, -1, 0, 1, 2, 3],
             [-6, -5, -4, 0, 4, 5, 6],
             [-9, -8, -7, 0, 7, 8, 9],
             [-12, -10, -9, 0, 9, 10, 12],
             [-9, -8, -7, 0, 7, 8, 9],
             [-6, -5, -4, 0, 4, 5, 6],
             [-3, -2, -1, 0, 1, 2, 3]], dtype=torch.float32
        ).view(1,1,7,7)

        sobel_kernel7_y = torch.tensor(
            [[3, 6, 9, 12, 9, 6, 3],
             [2, 5, 8, 10, 8, 5, 2],
             [1, 4, 7, 9, 7, 4, 1],
             [0, 0, 0, 0, 0, 0, 0],
             [-1, -4, -7, -9, -7, -4, -1],
             [-2, -5, -8, -10, -8, -5, -2],
             [-3, -6, -9, -12, -9, -6, -3]], dtype=torch.float32
        ).view(1,1,7,7)


        # 将卷积核扩展到多个通道
        sobel_kernel3_x = sobel_kernel3_x.repeat(in_channels, in_channels, 1, 1)
        sobel_kernel3_y = sobel_kernel3_y.repeat(in_channels, in_channels, 1, 1)

        sobel_kernel5_x = sobel_kernel5_x.repeat(in_channels, in_channels, 1, 1)
        sobel_kernel7_x = sobel_kernel7_x.repeat(in_channels, in_channels, 1, 1)
        sobel_kernel5_y = sobel_kernel5_y.repeat(in_channels, in_channels, 1, 1)
        sobel_kernel7_y = sobel_kernel7_y.repeat(in_channels, in_channels, 1, 1)

        self.sobel3_x.weight = torch.nn.Parameter(sobel_kernel3_x, requires_grad=False)
        self.sobel3_y.weight = torch.nn.Parameter(sobel_kernel3_y, requires_grad=False)
        self.sobel5_x.weight = torch.nn.Parameter(sobel_kernel5_x, requires_grad=False)
        self.sobel5_y.weight = torch.nn.Parameter(sobel_kernel5_y, requires_grad=False)
        self.sobel7_x.weight = torch.nn.Parameter(sobel_kernel7_x, requires_grad=False)
        self.sobel7_y.weight = torch.nn.Parameter(sobel_kernel7_y, requires_grad=False)

        self.sobelbn = torch.nn.InstanceNorm2d(in_channels * 3)
        self.sobelbn3 = torch.nn.InstanceNorm2d(in_channels * 3)
        self.sobelbn5 = torch.nn.InstanceNorm2d(in_channels * 3)
        self.sobelbn7 = torch.nn.InstanceNorm2d(in_channels * 3)

        self.CA = ChannelAttention(in_channels * 12)
        self.SA = SpatialAttention()
        self.PA = PixelAttention(in_channels * 12)



        # 定义线性变换
        self.conv33 = torch.nn.Conv2d(in_channels=in_channels * 12, out_channels=in_channels, kernel_size=3, padding=1, bias=True)
        self.bn3 = torch.nn.InstanceNorm2d(in_channels)
        self.conv55 = torch.nn.Conv2d(in_channels=in_channels * 12, out_channels=in_channels, kernel_size=5, padding=2, bias=True)
        self.bn5 = torch.nn.InstanceNorm2d(in_channels)
        self.conv77 = torch.nn.Conv2d(in_channels=in_channels * 12, out_channels=in_channels, kernel_size=7, padding=3, bias=True)
        self.bn7 = torch.nn.InstanceNorm2d(in_channels)

        self.leaky_relu = torch.nn.LeakyReLU(negative_slope=0.2)  # 设置负斜率为 0.01

        self.score_conv = torch.nn.Conv2d(in_channels=in_channels * 3, out_channels=in_channels, kernel_size=1, bias=True)
        self.bnscore = torch.nn.InstanceNorm2d(in_channels)


    def forward(self, input):
        epsilon = 1e-6
        edge_x = self.sobel_h(input)
        edge_y = self.sobel_v(input)
        angles = torch.atan2(edge_y, edge_x + epsilon)
        sobel = torch.cat((edge_x, edge_y, angles), dim=1)
        sobel = self.sobelbn(sobel)




        edge3_x = self.sobel3_x(input)
        edge3_y = self.sobel3_y(input)
        angles3 = torch.atan2(edge3_y, edge3_x + epsilon)
        sobel3 = torch.cat((edge3_x, edge3_y, angles3), dim=1)
        sobel3 = self.sobelbn3(sobel3)



        edge5_x = self.sobel5_x(input)
        edge5_y = self.sobel5_y(input)
        angles5 = torch.atan2(edge5_y, edge5_x + epsilon)
        sobel5 = torch.cat((edge5_x, edge5_y, angles5), dim=1)
        sobel5 = self.sobelbn5(sobel5)

        edge7_x = self.sobel7_x(input)
        edge7_y = self.sobel7_y(input)
        angles7 = torch.atan2(edge7_y, edge7_x + epsilon)
        sobel7 = torch.cat((edge7_x, edge7_y, angles7), dim=1)
        sobel7 = self.sobelbn7(sobel7)

        x = torch.cat((sobel, sobel3, sobel5, sobel7), dim=1)
        x = x / x.size(1)
        ca = self.CA(x)
        sa = self.SA(x)

        csa = ca + sa

        pa = self.PA(x, csa)

        x = x + pa




        # batch_size, channels, height, width = x.size()
        # 整合不同感受野的信息
        attention_33 = self.leaky_relu(self.bn3(self.conv33(x)))
        attention_55 = self.leaky_relu(self.bn5(self.conv55(x)))
        attention_77 = self.leaky_relu(self.bn7(self.conv77(x)))
        attention_core = self.bnscore(self.score_conv(torch.cat((attention_33, attention_55, attention_77), dim=1)))
        # output = torch.sigmoid(attention_core)
        return attention_core

