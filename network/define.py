import torch as torch
import json
import math
class Net():
    def __init__(self,jsonData=''):
        with open('./network/template/module.conf')as f:
            jsonData=f.read()
        self.data=json.loads(jsonData)
    def get_layer(self):
        if self.data['type']=='Conv2d':
            pass
    @staticmethod
    def forward(input,data):
        res=[]
        if data["type"]=='Conv':
            kerner_size=data["kerner_size"].replace('(','').replace(')','').split(',')
            stride = data["stride"].replace('(', '').replace(')', '').split(',')
            padding = data["padding"].replace('(', '').replace(')', '').split(',')
            dilation = data["dilation"].replace('(', '').replace(')', '').split(',')
            res=[-1,int(data['out_channels'])]
            for i in range(data['dimension']):
                out=math.floor( (int(input[i+2]) + 2*int(padding[i])-
                                 int(dilation[i])*(int(kerner_size[i])-1)-1)/int(stride[i]))+1
                res.append(out)
        elif data["type"]=='MaxPool' or data["type"]=='AvgPool':
            kerner_size = data["kerner_size"].replace('(', '').replace(')', '').split(',')
            stride = data["stride"].replace('(', '').replace(')', '').split(',')
            padding = data["padding"].replace('(', '').replace(')', '').split(',')
            dilation = data["dilation"].replace('(', '').replace(')', '').split(',')
            res = [input[0], input[1]]
            for i in range(data['dimension']):
                out=math.floor( (int(input[i+2]) + 2*int(padding[i])-
                                 int(dilation[i])*(int(kerner_size[i])-1)-1)/int(stride[i]))+1
                res.append(out)
            pass
        elif data["type"]=='Linear':
            res=[-1,int(data['output_num'])]
        else:
            return input
        return res
    @staticmethod
    def code_write(path,table,content):
        with open(path,'a') as f:
            f.write('    '*table+content+'\n')
    def code_gen(self):
        path='./network/template/net.py'

        with open('./network/template/net.py','w') as f:
            with open('./network/template/head', 'r') as f1:
                content = f1.read()
                print(111)
                print(content)
                f.write(content)
            with open('./network/template/init', 'r') as f1:
                content = f1.read()
                f.write(content)
            input_str=self.data['input_size'].replace('(', '').replace(')', '').split(',')
            input=list(map(int,input_str))
            for i,layer in enumerate(self.data['layers']):
                if layer['type']=='Conv':
                    print('self.layer%d=nn.Conv%dd(in_channels=%s,out_channels=%s,kernel_size=%s,'
                                          'stride=%s,padding=%s,dilation=%s)'
                                   %(i,layer['dimension'],input[1],layer['out_channels'],layer['kerner_size'],
                                     layer['stride'],layer['padding'],layer['dilation']))
                    Net.code_write(path,2,'self.layer%d=nn.Conv%dd(in_channels=%s,out_channels=%s,kernel_size=%s,'
                                          'stride=%s,padding=%s,dilation=%s)'
                                   %(i,layer['dimension'],input[1],layer['out_channels'],layer['kerner_size'],
                                     layer['stride'],layer['padding'],layer['dilation']))

                elif layer['type']=='MaxPool':
                    Net.code_write(path,2,'self.layer%d=nn.MaxPool%dd(kernel_size=%s, stride=%s, padding=%s, '
                                          'dilation=%s)'%(i,layer['dimension'],layer['kerner_size'],
                                     layer['stride'],layer['padding'],layer['dilation']))

                elif layer['type']=='AvgPool':
                    Net.code_write(path, 2, 'self.layer%d=nn.AvgPool%dd(kernel_size=%s, stride=%s, padding=%s, '
                                            'dilation=%s)' % (i, layer['dimension'], layer['kerner_size'],
                                                              layer['stride'], layer['padding'], layer['dilation']))
                    pass
                elif layer['type']=='ReLU':
                    Net.code_write(path,2,'self.layer%d=nn.ReLU()'%(i))
                    pass
                elif layer['type'] == 'ReLU6':
                    Net.code_write(path, 2, 'self.layer%d=nn.ReLU6()' % (i))
                    pass
                elif layer['type'] == 'ELU':
                    Net.code_write(path, 2, 'self.layer%d=nn.ELU()' % (i))
                    pass
                elif layer['type'] == 'PReLU':
                    Net.code_write(path, 2, 'self.layer%d=nn.PReLU()' % (i))
                    pass
                elif layer['type'] == 'Sigmoid':
                    Net.code_write(path, 2, 'self.layer%d=nn.Sigmoid()' % (i))
                    pass
                elif layer['type'] == 'Threshold':
                    Net.code_write(path, 2, 'self.layer%d=nn.Threshold(threshold=%s, value=%s)' %
                                   (i,layer['threshold'],layer['value']))
                    pass
                elif layer['type'] == 'Tanh':
                    Net.code_write(path, 2, 'self.layer%d=nn.Tanh()' % (i))
                    pass
                elif layer['type'] == 'LogSigmoid':
                    Net.code_write(path, 2, 'self.layer%d=nn.LogSigmoid()' % (i))
                    pass
                elif layer['type'] == 'Softmax':
                    Net.code_write(path, 2, 'self.layer%d=nn.Softmax()' % (i))
                    pass
                elif layer['type'] == 'BatchNorm':
                    Net.code_write(path, 2, 'self.layer%d=nn.BatchNorm%dd(%s)' % (i,layer['dimension'],layer['num_features']))
                    pass
                elif layer['type'] == 'Linear':
                    Net.code_write(path, 2, 'self.layer%d=nn.Linear(%s,%s)' % (i,input[2],layer['output_num']))
                    pass
                input=Net.forward(input,layer)
                print(input,i)
                pass
            with open('./network/template/formwrd', 'r') as f1:
                content = f1.read()
                f.write(content)

jsonData = '{' \
           '"type":"Conv2d",' \
           '"out_channels":2,' \
           '"kerner_size":3,' \
           '"stride":4,' \
           '"padding":5}'
jsondata='{"input_size":"(3,28,28)","layers":[{"type":"Conv1d","out_channels":2,"kerner_size":"(3,)",'\
			'"stride":"(1,)","padding":"(1,)"},{"type":"Conv","out_channels":10,"kerner_size":"(3,5)","stride":"(2,1)","padding":"(4,2)","dilation":"(3, 1)","dimension":2},'\
		'{"type":"Conv3d","out_channels":2,"kerner_size":"(3,3,3)","stride":"(1,1,1)","padding":"(1,1,1)"}]}'

data=json.loads(jsondata)
print(data['layers'][1])
print(Net.forward([20, 16, 50, 100],data['layers'][1]),)
a=Net()
a.code_gen()