import torch 
import torchvision
import os
import argparse
# from utils_MHGAN import pick_up_real_samples, mh_samples, load_model_G, load_model_D, load_model_C
# from torchvision import datasets, transforms
# import time


from model import Generator, Discriminator, Calibrator_linear
from utils import load_model

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate Normalizing Flow.')
    parser.add_argument("--batch_size", type=int, default=2048,
                      help="The batch size to use for training.")
    args = parser.parse_args()




    print('Model Loading...')
    # Model Pipeline
    mnist_dim = 784

    model = Generator(g_output_dim = mnist_dim).cuda()
    model = load_model(model, 'checkpoints', point="G.pth")
    model = torch.nn.DataParallel(model).cuda()
    model.eval()
    
    # Discr = Discriminator(mnist_dim).cuda()
    # Discr = load_model(Discr, 'checkpoints/', point="D.pth")
    # Discr = torch.nn.DataParallel(Discr).cuda()
    # Discr.eval()

    print('Model loaded.')



    print('Start Generating')
    os.makedirs('samples', exist_ok=True)

    # NORMAL GENERATION :
    n_samples = 0
    with torch.no_grad():
        while n_samples<10000:
            z = torch.randn(args.batch_size, 100).cuda()
            x = model(z)
            x = x.reshape(args.batch_size, 28, 28)
            for k in range(x.shape[0]):
                if n_samples<10000:
                    torchvision.utils.save_image(x[k:k+1], os.path.join('samples', f'{n_samples}.png'))         
                    n_samples += 1


    # MHGAN GENERATION :

    # Calib = Calibrator_linear().cuda()
    # Calib = load_model_C(Calib, 'checkpoints')
    # Calib = torch.nn.DataParallel(Calib).cuda()
    # Calib.eval()

    # # Loading dataset for MHGAN sampling:
    # transform = transforms.Compose([
    #         transforms.ToTensor(),
    #         transforms.Normalize(mean=(0.5), std=(0.5))])
    # test_dataset = datasets.MNIST(root='data/MNIST/', train=False, transform=transform, download=True)
    # test_loader = torch.utils.data.DataLoader(dataset=test_dataset, 
    #                                           batch_size=1, shuffle=True)
    
    # n_samples = 0
    # K = 10
    # with torch.no_grad():
    #     # t_start = time.time()
    #     while n_samples<10000:
    #         x0 = torch.zeros((2, mnist_dim)).cuda()
    #         x_real = pick_up_real_samples(test_loader)
    #         x0[0,:] = x_real.view(-1, mnist_dim).reshape(1, mnist_dim).cuda()
    #         new_sample = mh_samples(x0, model, Discr, Calib, K, f"plot{n_samples}")
    #         torchvision.utils.save_image(new_sample, os.path.join('samples', f'{n_samples}.png'))
    #         n_samples += 1
    
    # building_time = time.time() - t_start
    # print(f'computation time = {building_time:.2f}s')


    # n_samples = 0
    # t_start = time.time()

    # with torch.no_grad():
        
    #     while n_samples<10000:
    #         x0 = pick_up_real_samples(1).cuda()
    #         x0 = x0.view(-1, mnist_dim)
    #         change = False # True when x0 actualized
    #         c = 0 
    #         for _ in range(10):  
    #             z = torch.randn(1, 100).cuda()
    #             x_pot = model(z)
    #             U = torch.rand(1).cuda() # draw a uniform variable between [0;1]
    #             ratio = (Discr(x0)**(-1) - 1) / (Discr(x_pot)**(-1) - 1)

    #             if U <= ratio:
    #                 change = True
    #                 c +=1
    #                 x0 = x_pot.clone()
                    
    #         if change == True:
    #             x_pot = x_pot.reshape(1, 28, 28)        
    #             torchvision.utils.save_image(x_pot[0], os.path.join('samples', f'{n_samples}.png'))         
    #             n_samples += 1
    #             print(f'Nombre de sample généré : {n_samples} | Nombre de generation acceptée : {c}')
    
    # building_time = time.time() - t_start
    # print(f'computation time = {building_time:.2f}s')