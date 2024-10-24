import torch
import os


def D_train(x, G, D, D_optimizer, criterion):
    #=======================Train the discriminator=======================#
    D.zero_grad()

    # train discriminator on real
    x_real, y_real = x, torch.ones(x.shape[0], 1)
    x_real, y_real = x_real, y_real

    D_output = D(x_real)
    D_real_loss = criterion(D_output, y_real)
    D_real_score = D_output

    # train discriminator on facke
    z = torch.randn(x.shape[0], 100)
    x_fake, y_fake = G(z), torch.zeros(x.shape[0], 1)

    D_output =  D(x_fake)
    
    D_fake_loss = criterion(D_output, y_fake)
    D_fake_score = D_output

    # gradient backprop & optimize ONLY D's parameters
    D_loss = D_real_loss + D_fake_loss
    D_loss.backward()
    D_optimizer.step()
        
    return  D_loss.data.item()


def G_train(x, G, D, G_optimizer, criterion, threshold):
    #=======================Train the generator=======================#
    G.zero_grad()

    z = torch.randn(x.shape[0], 100)  # Latent space sample (input for G)
    y_real_labels = torch.ones(x.shape[0], 1)  # Real labels

    G_output = G(z)  # Generate fake samples
    D_output = D(G_output)  # Discriminator's evaluation of fake samples
    G_loss = criterion(D_output, y_real_labels)  # Generator's loss

    quotient = D_output/(1-D_output)

    # Sample rejection process based on threshold
    # Re-generate samples until the discriminator's output is above a certain threshold
    with torch.no_grad():  # No need to track gradients during sample rejection
        while torch.mean(quotient) < threshold:
            z = torch.randn(x.shape[0], 100)  # Re-sample latent space
            G_output = G(z)  # Re-generate fake samples
            D_output = D(G_output)  # Get new discriminator output
            G_loss = criterion(D_output, y_real_labels)  # Re-calculate generator's loss
            quotient = D_output/(1-D_output)
    
    # Once acceptable samples are generated, optimize G's parameters
    G_loss.backward()
    G_optimizer.step()

    return G_loss.item()




def save_models(G, D, folder):
    torch.save(G.state_dict(), os.path.join(folder,'G.pth'))
    torch.save(D.state_dict(), os.path.join(folder,'D.pth'))


def load_model(G, folder):
    ckpt = torch.load(os.path.join(folder,'G.pth'))
    G.load_state_dict({k.replace('module.', ''): v for k, v in ckpt.items()})
    return G
