#!/usr/bin/python

import os,sys,pprint
class Tree(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value

try:
   input_file=sys.argv[1]
except:
    print('Usage : "./process_trade.py <input_file>.csv <output_flle>.csv"')
    exit()  

try:
   output_flle=sys.argv[2]
except:
    print('Usage : "./process_trade.py <input_file>.csv <output_flle>.csv"')
    exit()

#Open input CSV and create a multidimentional data structure with symbol as key
#<TimeStamp>,<Symbol>,<Quantity>,<Price>
def build_trade_structure(trades,input_file):
    with open (input_file, "r") as file:
        for line in file:
            line = line.strip()
            line = line.split(',')
            symbol = str(line[1])
            TimeStamp = int(line[0])
            Qty = int(line[2])            
            Value = int(line[3])
            
            ## Build an array with timestamp for each trades
            if not trades[symbol]['times']:
                trades[symbol]['times'] = []              
            trades[symbol]['times'].append(TimeStamp)            

            ## Declare araay for timegap between consicutive trades
            if not trades[symbol]['TimeGap']:
                trades[symbol]['TimeGap'] = []
            
            ## Build an array with timegap between consicutive trades
            if len(trades[symbol]['times']) > 1:                
                TimeGap = TimeStamp - trades[symbol]['times'][-2]                
                trades[symbol]['TimeGap'].append(TimeGap)            

            ## Calculate Total Volume of each symbol
            trades[symbol][TimeStamp]['Quantity'] = Qty
            if trades[symbol]['Volume']:
                trades[symbol]['Volume'] += Qty
            else:
                trades[symbol]['Volume'] = 0
                trades[symbol]['Volume'] += Qty
            
            ## Calculate Total trade value of each symbol
            trades[symbol][TimeStamp]['TradeValue'] = Value * Qty
            if trades[symbol]['TotalTradeValue']:
                trades[symbol]['TotalTradeValue'] += trades[symbol][TimeStamp]['TradeValue']
            else:
                trades[symbol]['TotalTradeValue'] = 0
                trades[symbol]['TotalTradeValue'] += trades[symbol][TimeStamp]['TradeValue']
          
            ## Build an array with price for each trades
            if not trades[symbol]['Prices']:
                trades[symbol]['Prices'] = []              
            trades[symbol]['Prices'].append(Value)
    file.close()
    return trades

## Calculate Weighted Avg Price, MaxPrice and MaxTimeGap
def derive_pricing(trades):    
    for symbol in trades:        
        trades[symbol]['WeightedAveragePrice'] = int(trades[symbol]['TotalTradeValue']/trades[symbol]['Volume'])
        trades[symbol]['MaxPrice'] = max(trades[symbol]['Prices'])
        trades[symbol]['MaxTimeGap'] = max(trades[symbol]['TimeGap'])
        ## Set MaxTimeGap to 0 for single trade for a perticulat symbol
        if len(trades[symbol]['times']) == 1 :
            print(symbol)
            trades[symbol]['MaxTimeGap'] = int(0)
    return trades

## Write output file
def write_op_file(trades,output_flle):
    file = open(output_flle, 'w+')
    for symbol in sorted(trades) :
        #<symbol>,<MaxTimeGap>,<Volume>,<WeightedAveragePrice>,<MaxPrice>
        file.write("%s,%s,%s,%s,%s\n"%(symbol,trades[symbol]['MaxTimeGap'],trades[symbol]['Volume'],trades[symbol]['WeightedAveragePrice'],trades[symbol]['MaxPrice']))
    file.close()


def main():
    if os.path.isfile(input_file):        
        trades = Tree()
        build_trade_structure(trades,input_file)
        derive_pricing(trades)
        write_op_file(trades,output_flle)
    else:
        print("Input file doesn't exist")
    #pprint.pprint(trades)

if __name__ == "__main__":
    main()