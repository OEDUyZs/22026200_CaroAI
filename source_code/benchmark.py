import time
import math
from source.AI import GomokuAI

# 5 thế cờ thử nghiệm (1 là máy đánh, -1 là người đánh)
states = [
    {"name": "1. Khởi cuộc", "moves": [(4,4,-1)]},
    {"name": "2. Giữa ván", "moves": [(4,4,-1), (4,5,1), (5,5,-1), (3,3,1), (5,4,-1)]},
    {"name": "3. Máy sắp thắng", "moves": [(4,4,-1), (4,5,1), (3,3,-1), (3,5,1), (2,2,-1), (2,5,1)]},
    {"name": "4. Người sắp thắng", "moves": [(4,4,-1), (5,4,1), (4,5,-1), (5,5,1), (4,6,-1)]},
    {"name": "5. Bẫy ngã ba", "moves": [(4,4,-1), (5,5,1), (4,5,-1), (5,6,1), (3,4,-1)]}
]

def run_benchmark():
    print("="*85)
    print(f"{'Trạng thái':<20} | {'Thuật toán':<12} | {'Depth':<5} | {'Thời gian (s)':<15} | {'Nodes đã duyệt':<15}")
    print("="*85)

    for s in states:
        for algo_name, algo_id in [('Minimax', 1), ('Alpha-Beta', 2)]:
            for depth in [1, 2, 3]:
                # Setup bàn cờ
                ai = GomokuAI(depth=depth)
                for (i, j, player) in s["moves"]:
                    ai.setState(i, j, player)
                    ai.updateBound(i, j, ai.nextBound)
                
                ai.nodeCount = 0
                
                start = time.time()
                if algo_id == 1:
                    ai.minimax(depth, ai.boardValue, ai.nextBound, True)
                else:
                    ai.alphaBetaPruning(depth, ai.boardValue, ai.nextBound, -math.inf, math.inf, True)
                end = time.time()
                
                t = round(end - start, 4)
                print(f"{s['name']:<20} | {algo_name:<12} | {depth:<5} | {t:<15} | {ai.nodeCount:<15}")
        print("-" * 85)

if __name__ == '__main__':
    run_benchmark()