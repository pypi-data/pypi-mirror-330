import torch
from tqdm import tqdm
import os
from torch import nn
from torch.utils.tensorboard import SummaryWriter

def tensorboard_writer(log_dir, score, loss):
    writer = SummaryWriter(log_dir=log_dir)
    writer.add_scalar(tag='test_result', scalar_value=score)
    return writer


# metric: 评价指标的方法
def test(model, testloader, criterion, metric=None):
    model.eval()  # 将模型设置为评估模式
    criterion = criterion.cuda()
    sum_loss = 0
    loop = enumerate(testloader)
    sum_metric = 0
    with torch.no_grad():  
        for i, (data, targets) in loop:
            scores = model(data)
            loss = criterion(scores, targets)
            sum_loss += loss.item()
            if metric is not None:
                m = metric(scores, targets)
                sum_metric += m

    print(f'metric:{sum_metric / (testloader.__len__())}')

    return sum_loss / (testloader.__len__())


def train(model, criterion, optimizer, trainloader, epochs, testloader,
          testEpoch, modelSavedPath='./checkpoint/',
          scheduler=None, checkpoint_path=None):

    if not os.path.exists(modelSavedPath):
        os.makedirs(modelSavedPath)
        print(f'{modelSavedPath} mkdir success')

    start_epoch = 0
    test_min_loss = 9e9

    if checkpoint_path is not None :
        if not os.path.exists(checkpoint_path):
            print(f"Checkpoint not found at {checkpoint_path}")

        print(f"Loading checkpoint from {checkpoint_path}")
        checkpoint = torch.load(checkpoint_path)
        model.load_state_dict(checkpoint['model_state_dict'])
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        start_epoch = checkpoint['epoch'] + 1

        if scheduler is not None and 'scheduler_state_dict' in checkpoint:
            scheduler.load_state_dict(checkpoint['scheduler_state_dict'])

        print(f"Resumed training from epoch {start_epoch}")

    model = model
    criterion = criterion
    if torch.cuda.is_available():
        model = model.cuda()
        criterion = criterion.cuda()

    for epoch in range(start_epoch, epochs):

        loop = tqdm(enumerate(trainloader), total=(len(trainloader)))
        loop.set_description(f'Epoch [{epoch}/{epochs}]')

        sum_loss = 0
        count = 0   

        for i, (data, targets) in loop:
            # forward
            scores = model(data)
            loss = criterion(scores, targets)

            sum_loss += loss.item()
            count += 1

            # backward
            optimizer.zero_grad()
            loss.backward()

            # gradient descent or adam step
            optimizer.step()

        print(f'train loss:{sum_loss / count}')

        if epoch % testEpoch == 0:

            test_loss = test(model, testloader, criterion)

            print(f'test loss:{test_loss}')

            if test_loss < test_min_loss:
                test_min_loss = test_loss
                # Save checkpoint
                checkpoint = {
                    'epoch': epoch,
                    'model_state_dict': model.state_dict(),
                    'optimizer_state_dict': optimizer.state_dict(),
                }
                if scheduler is not None:
                    checkpoint['scheduler_state_dict'] = scheduler.state_dict()
                torch.save(checkpoint, os.path.join(modelSavedPath, f'checkpoint_{epoch}.pth'))
                print(f'Checkpoint saved at epoch {epoch}')

        # test后再scheduler
        if scheduler is not None:
            scheduler.step()
    checkpoint = {
        'epoch': epoch,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
    }
    if scheduler is not None:
        checkpoint['scheduler_state_dict'] = scheduler.state_dict()
    torch.save(checkpoint, os.path.join(modelSavedPath, 'latest.pth'))
    print(f'Checkpoint saved at epoch {epoch}')

    torch.save(model.state_dict(), os.path.join(modelSavedPath, f'{epoch}_model.pkl'))