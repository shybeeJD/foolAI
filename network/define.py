import torch as torch
import json
import math
class Conv2d():
    def __init__(self,jsonData):
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
        return res

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
print(Conv2d.forward([20, 16, 50, 100],data['layers'][1]),)