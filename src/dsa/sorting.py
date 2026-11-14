from typing import List, Dict, Any

def rank_strategies(strategies_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:

    def compare(left_item: Dict, right_item: Dict) -> bool:
        if left_item.get('win_rate', 0) != right_item.get('win_rate', 0):
            return left_item.get('win_rate', 0) > right_item.get('win_rate', 0)
        
        if left_item.get('pnl', 0) != right_item.get('pnl', 0):
            return left_item.get('pnl', 0) > right_item.get('pnl', 0)
            
        return left_item.get('max_drawdown', float('inf')) < right_item.get('max_drawdown', float('inf'))

    def merge(left: List[Dict], right: List[Dict]) -> List[Dict]:
        merged = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if compare(left[i], right[j]):
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
                
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged

    def merge_sort(arr: List[Dict]) -> List[Dict]:
        if len(arr) <= 1:
            return arr
            
        mid = len(arr) // 2
        left_half = merge_sort(arr[:mid])
        right_half = merge_sort(arr[mid:])
        
        return merge(left_half, right_half)

    return merge_sort(strategies_results)