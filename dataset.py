from __future__ import print_function
import torch
import torchvision.datasets as dset
import torchvision.transforms as transforms


def get_dataloader(opt):
    if opt.dataset in ['imagenet', 'folder', 'lfw']:
        # list transformation operations
        transform_ops = [
            transforms.Scale(opt.imageScaleSize),
            transforms.CenterCrop(opt.imageSize),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
        ]

        # force convert to grayscale when number of channels is 1
        if opt.nc == 1:
            transform_ops.insert(0, transforms.Grayscale())

        # load dataset folder with transformations
        dataset = dset.ImageFolder(root=opt.dataroot,
                                   transform=transforms.Compose(transform_ops)
                                   )
    elif opt.dataset == 'lsun':
        dataset = dset.LSUN(db_path=opt.dataroot, classes=['bedroom_train'],
                            transform=transforms.Compose([
                                transforms.Scale(opt.imageScaleSize),
                                transforms.CenterCrop(opt.imageSize),
                                transforms.ToTensor(),
                                transforms.Normalize((0.5, 0.5, 0.5),
                                                     (0.5, 0.5, 0.5)),
                            ]))
    elif opt.dataset == 'cifar10':
        dataset = dset.CIFAR10(root=opt.dataroot, download=True,
                               transform=transforms.Compose([
                                   transforms.Scale(opt.imageSize),
                                   transforms.ToTensor(),
                                   transforms.Normalize((0.5, 0.5, 0.5),
                                                        (0.5, 0.5, 0.5)),
                               ])
                               )
    assert dataset
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=opt.batch_size,
                                             shuffle=opt.shuffle,
                                             num_workers=int(opt.workers))
    return dataloader
