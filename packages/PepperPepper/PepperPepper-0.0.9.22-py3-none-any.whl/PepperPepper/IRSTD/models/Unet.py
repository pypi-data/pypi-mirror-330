from PepperPepper.environment import torch, nn, profile
from PepperPepper.layers import ResidualBlock, _FCNHead, Coopetition_Fuse, Global_Context_Mamba_Bridge



class UNet(nn.Module):
    def __init__(self,
                 img_size=256,
                 in_dims=3,
                 num_classes = 1,
                 dim=32,
                 depth=2
                 ):
        super().__init__()
        self.title = 'UNet_CPF_GCMB'
        self.in_dims = in_dims
        self.num_classes = num_classes
        self.dim = dim
        self.depth = depth
        self.img_size = img_size

        self.stem = ResidualBlock(in_dims, dim)
        self.pool = nn.MaxPool2d(2, 2)
        self.up = nn.Upsample(scale_factor=2)
        self.GCMB = Global_Context_Mamba_Bridge(img_size=img_size, patch_size=1, depths=[dim, dim*2, dim*4, dim*8])


        self.downlayer1 = ResidualBlock(dim, dim * 2)
        self.downlayer2 = ResidualBlock(dim * 2, dim * 4)
        self.downlayer3 = ResidualBlock(dim * 4, dim * 8)
        self.downlayer4 = ResidualBlock(dim * 8, dim * 16)

        self.upconv3 = nn.Sequential(
            nn.Upsample(scale_factor=2),
            nn.Conv2d(dim * 16, dim * 8, kernel_size=1),
        )
        self.upfuse3 = nn.Sequential(
            Coopetition_Fuse(3),
        )
        self.uplayer3 = ResidualBlock(dim * 8, dim * 8)



        self.upconv2 = nn.Sequential(
            nn.Upsample(scale_factor=2),
            nn.Conv2d(dim * 8, dim * 4, kernel_size=1),
        )
        self.upfuse2 = nn.Sequential(
            Coopetition_Fuse(3),
        )
        self.uplayer2 = ResidualBlock(dim * 4, dim * 4)




        self.upconv1 = nn.Sequential(
            nn.Upsample(scale_factor=2),
            nn.Conv2d(dim * 4, dim * 2, kernel_size=1),
        )
        self.upfuse1 = nn.Sequential(
            Coopetition_Fuse(3),
        )
        self.uplayer1 = ResidualBlock(dim * 2, dim * 2)




        self.upconv0 = nn.Sequential(
            nn.Upsample(scale_factor=2),
            nn.Conv2d(dim * 2, dim, kernel_size=1),
        )
        self.upfuse0 = nn.Sequential(
            Coopetition_Fuse(3),
        )

        self.outc = _FCNHead(dim, num_classes)


    def forward(self, x):
        # check the dims
        if x.size()[1] == 1:
            x = x.repeat(1, self.in_dims, 1, 1)

        f0 = self.stem(x)
        f1 = self.downlayer1(self.pool(f0))
        f2 = self.downlayer2(self.pool(f1))
        f3 = self.downlayer3(self.pool(f2))
        f4 = self.downlayer4(self.pool(f3))

        global_f = self.GCMB([f0, f1, f2, f3])

        # for f in global_f:
        #     print(f.shape)



        d3 = self.uplayer3(self.upfuse3([self.upconv3(f4), f3, global_f[-1]]))
        d2 = self.uplayer2(self.upfuse2([self.upconv2(d3), f2, global_f[-2]]))
        d1 = self.uplayer1(self.upfuse1([self.upconv1(d2), f1, global_f[-3]]))
        out  = self.outc(self.upfuse0([self.upconv0(d1), f0, global_f[-4]]))
        return out






if __name__ == '__main__':
    model = UNet().cuda()
    inputs = torch.rand(1, 1, 256, 256).cuda()
    output = model(inputs)
    print(output.shape)
    flops, params = profile(model, (inputs,))

    print("-" * 50)
    print('FLOPs = ' + str(flops / 1000 ** 3) + ' G')
    print('Params = ' + str(params / 1000 ** 2) + ' M')