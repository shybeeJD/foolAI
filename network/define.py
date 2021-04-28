
import json
import math
import os
def exception_handle(error=''):
    print('error:'+error)

class Net():
    def __init__(self,jsonData=''):
        with open('./template/module.conf')as f:
            jsonData=f.read()
        self.data=json.loads(jsonData)
        self.shape=[]
    def get_layer(self):
        if self.data['type']=='Conv2d':
            pass
    def num_flat_features(self,x):
        #x.size()返回值为(256, 16, 5, 5)，size的值为(16, 5, 5)，256是batch_size
        size = x[1:]        #x.size返回的是一个元组，size表示截取元组中第二个开始的数字
        num_features = 1
        for s in size:
            num_features *= s
        return num_features 

    @staticmethod
    def forward(input_,data):
        res=[]
        if data["type"]=='Conv':
            kerner_size=data["kerner_size"].replace('(','').replace(')','').split(',')
            stride = data["stride"].replace('(', '').replace(')', '').split(',')
            padding = data["padding"].replace('(', '').replace(')', '').split(',')
            dilation = data["dilation"].replace('(', '').replace(')', '').split(',')
            res=[-1,int(data['out_channels'])]
            for i in range(data['dimension']):
                out=math.floor( (int(input_[i+2]) + 2*int(padding[i])-
                                 int(dilation[i])*(int(kerner_size[i])-1)-1)/int(stride[i]))+1
                res.append(out)
        elif data["type"]=='MaxPool' or data["type"]=='AvgPool':
            kerner_size = data["kerner_size"].replace('(', '').replace(')', '').split(',')
            stride = data["stride"].replace('(', '').replace(')', '').split(',')
            padding = data["padding"].replace('(', '').replace(')', '').split(',')
            dilation = data["dilation"].replace('(', '').replace(')', '').split(',')
            res = [input_[0], input_[1]]
            for i in range(data['dimension']):
                out=math.floor( (int(input_[i+2]) + 2*int(padding[i])-
                                 int(dilation[i])*(int(kerner_size[i])-1)-1)/int(stride[i]))+1
                res.append(out)
            pass
        elif data["type"]=='Linear':
            res=[-1,int(data['output_num'])]
        else:
            return input_
        return res
    @staticmethod
    def code_write(file,table,content):
        file.write('    '*table+content+'\n\r')
    def code_gen(self):
        path='./template/net.py'

        with open('./template/net.py','w') as f:
            with open('./template/head', 'r') as f1:
                content = f1.read()
                f.write(content)
            with open('./template/init', 'r') as f1:
                content = f1.read()
                f.write(content)
                f.write('\n\r')
            input_str=self.data['input_size'].replace('(', '').replace(')', '').split(',')
            input_=list(map(int,input_str))
            self.shape.append(input_)
            for i,layer in enumerate(self.data['layers']):
                if layer['type']=='Conv':
                    print('self.layer%d=nn.Conv%dd(in_channels=%s,out_channels=%s,kernel_size=%s,'
                                          'stride=%s,padding=%s,dilation=%s)'
                                   %(i,layer['dimension'],layer['in_channels'],layer['out_channels'],layer['kerner_size'],
                                     layer['stride'],layer['padding'],layer['dilation']))
                    Net.code_write(f,2,'self.layer%d=nn.Conv%dd(in_channels=%s,out_channels=%s,kernel_size=%s,'
                                          'stride=%s,padding=%s,dilation=%s)'
                                   %(i,layer['dimension'],layer['in_channels'],layer['out_channels'],layer['kerner_size'],
                                     layer['stride'],layer['padding'],layer['dilation']))

                elif layer['type']=='MaxPool':
                    Net.code_write(f,2,'self.layer%d=nn.MaxPool%dd(kernel_size=%s, stride=%s, padding=%s, '
                                          'dilation=%s)'%(i,layer['dimension'],layer['kerner_size'],
                                     layer['stride'],layer['padding'],layer['dilation']))

                elif layer['type']=='AvgPool':
                    Net.code_write(f, 2, 'self.layer%d=nn.AvgPool%dd(kernel_size=%s, stride=%s, padding=%s, '
                                            'dilation=%s)' % (i, layer['dimension'], layer['kerner_size'],
                                                              layer['stride'], layer['padding'], layer['dilation']))
                    pass
                elif layer['type']=='ReLU':
                    Net.code_write(f,2,'self.layer%d=nn.ReLU()'%(i))
                    pass
                elif layer['type'] == 'ReLU6':
                    Net.code_write(f, 2, 'self.layer%d=nn.ReLU6()' % (i))
                    pass
                elif layer['type'] == 'ELU':
                    Net.code_write(f, 2, 'self.layer%d=nn.ELU()' % (i))
                    pass
                elif layer['type'] == 'PReLU':
                    Net.code_write(f, 2, 'self.layer%d=nn.PReLU()' % (i))
                    pass
                elif layer['type'] == 'Sigmoid':
                    Net.code_write(f, 2, 'self.layer%d=nn.Sigmoid()' % (i))
                    pass
                elif layer['type'] == 'Threshold':
                    Net.code_write(f, 2, 'self.layer%d=nn.Threshold(threshold=%s, value=%s)' %
                                   (i,layer['threshold'],layer['value']))
                    pass
                elif layer['type'] == 'Tanh':
                    Net.code_write(f, 2, 'self.layer%d=nn.Tanh()' % (i))
                    pass
                elif layer['type'] == 'LogSigmoid':
                    Net.code_write(f, 2, 'self.layer%d=nn.LogSigmoid()' % (i))
                    pass
                elif layer['type'] == 'Softmax':
                    Net.code_write(f, 2, 'self.layer%d=nn.Softmax()' % (i))
                    pass
                elif layer['type'] == 'BatchNorm':
                    Net.code_write(f, 2, 'self.layer%d=nn.BatchNorm%dd(%s)' % (i,layer['dimension'],layer['num_features']))
                    pass
                elif layer['type'] == 'Linear':
                    Net.code_write(f, 2, 'self.layer%d=nn.Linear(%s,%s)' % (i,layer['input_num'],layer['output_num']))
                    pass
                input_=Net.forward(input_,layer)
                print(input_)
                self.shape.append(input_)

            print(self.shape)
            Net.code_write(f,1,'def forward(self, x):')

            
            for i,layer in enumerate(self.data['layers']):
                if layer['type']=='Conv':
                    print(self.shape[i],layer['dimension']+1)
                    if len(self.shape[i])!=layer['dimension']+2:
                        exception_handle('卷基层输入维度错误')
                    elif self.shape[i][1]!=layer['in_channels']:
                        exception_handle('输入通道数错误')
                    else:
                        Net.code_write(f,2,'x=self.layer%d(x)'%(i))
                elif layer['type'] == 'Linear':
                    if self.num_flat_features(self.shape[i])%layer['input_num']!=0:
                        exception_handle('无法展平')
                    else:
                        Net.code_write(f,2,'x=x.view(-1,%s)(x)'%(layer['input_num']))
                        Net.code_write(f,2,'x=self.layer%d(x)'%(i))
                else:
                    Net.code_write(f,2,'x=self.layer%d(x)'%(i))



                    pass

            Net.code_write(f,2,'return x')

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
print(os.system('pwd'))
print(data['layers'][1])
print(Net.forward([20, 16, 50, 100],data['layers'][1]),)
a=Net()
a.code_gen()