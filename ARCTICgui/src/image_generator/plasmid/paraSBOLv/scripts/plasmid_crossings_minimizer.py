"""
Edge crossing minimization algorithms for plasmid diagrams.
Focuses on reducing  connection crossings in visualizations.
"""
import itertools
import random

def estimate_crossing_difficulty(group):
    """
    Estimate how likely a group is to cause crossings.
    
    Args:
        group: List of connection definitions with x-coordinates
        
    Returns:
        A difficulty score (higher means more likely to cause crossings)
    """
    # If no connections, return 0
    if not group:
        return 0
    
    # Get the span of the connections - how wide do they go
    min_x = float('inf')
    max_x = float('-inf')
    for conn in group:
        if 'source_x' in conn and 'target_x' in conn:
            min_x = min(min_x, conn['source_x'], conn['target_x'])
            max_x = max(max_x, conn['source_x'], conn['target_x'])
    
    # If no x-coordinates, return 0
    if min_x == float('inf') or max_x == float('-inf'):
        return 0
        
    # Difficulty is proportional to horizontal span
    span = max_x - min_x
    
    # Also consider how many top/bottom connections we have
    top_connections = sum(1 for c in group if c['source_row'] == 0 or c['target_row'] == 0)
    bottom_connections = sum(1 for c in group if c['source_row'] == 1 or c['target_row'] == 1)
    
    # Groups with more connections to both rows are more likely to cause crossings
    row_mix_factor = min(top_connections, bottom_connections) / max(1, len(group))
    
    return span * (1.0 + row_mix_factor * 2.0)

def count_crossings(connections):
    """
    Count the number of crossings between connections.
    
    Args:
        connections: List of connection dictionaries with source and target positions
        
    Returns:
        Number of crossings
    """
    crossings = 0
    # For each pair of connections
    for i in range(len(connections)):
        for j in range(i+1, len(connections)):
            conn1 = connections[i]
            conn2 = connections[j]
            
            # Skip if missing x-coordinates
            if not ('source_x' in conn1 and 'target_x' in conn1 and 
                   'source_x' in conn2 and 'target_x' in conn2):
                continue
            
            # Get endpoints 
            x1_left = min(conn1['source_x'], conn1['target_x'])
            x1_right = max(conn1['source_x'], conn1['target_x']) 
            
            x2_left = min(conn2['source_x'], conn2['target_x'])
            x2_right = max(conn2['source_x'], conn2['target_x'])
            
            # Check if the x-ranges overlap
            if not (x1_right < x2_left or x2_right < x1_left):
                # Check if different rows (which causes a crossing)
                if ((conn1['source_row'] != conn2['source_row'] and 
                     conn1['target_row'] != conn2['target_row']) or
                    (conn1['source_row'] != conn2['target_row'] and
                     conn1['target_row'] != conn2['source_row'])):
                    # We have a crossing
                    crossings += 1
                    
    return crossings

def has_vertical_vertical_crossings(order, connection_groups):
    """
    Check if a specific ordering of groups would cause vertical-vertical crossings.
    
    Returns:
        True if vertical-vertical crossings exist, False otherwise
    """
    # Assign virtual y-levels based on the order
    group_y_levels = {group_id: i for i, group_id in enumerate(order)}
    
    # For each pair of groups, check if their vertical segments would cross
    for i, group1_id in enumerate(order):
        for j, group2_id in enumerate(order):
            if i >= j:  # Skip same group and already checked pairs
                continue
                
            group1 = connection_groups[group1_id]
            group2 = connection_groups[group2_id]
            
            # Get the y-level for each group
            y1 = group_y_levels[group1_id]
            y2 = group_y_levels[group2_id]
            
            # Check for vertical crossings between these two groups
            for conn1 in group1:
                if not ('source_x' in conn1 and 'target_x' in conn1):
                    continue
                    
                for conn2 in group2:
                    if not ('source_x' in conn2 and 'target_x' in conn2):
                        continue
                    
                    # Check if there could be a vertical-vertical crossing
                    # This happens when two vertical segments from different groups
                    # are at the same x-coordinate and their group ordering doesn't
                    # match their x-coordinate ordering
                    
                    # Check source-source vertical segments (if in same row)
                    if conn1['source_row'] == conn2['source_row']:
                        x1 = conn1['source_x']
                        x2 = conn2['source_x']
                        if (x1 < x2 and y1 > y2) or (x1 > x2 and y1 < y2):
                            return True
                    
                    # Check target-target vertical segments (if in same row)
                    if conn1['target_row'] == conn2['target_row']:
                        x1 = conn1['target_x']
                        x2 = conn2['target_x']
                        if (x1 < x2 and y1 > y2) or (x1 > x2 and y1 < y2):
                            return True
                    
                    # Check source-target vertical segments (if in same row)
                    if conn1['source_row'] == conn2['target_row']:
                        x1 = conn1['source_x']
                        x2 = conn2['target_x']
                        if (x1 < x2 and y1 > y2) or (x1 > x2 and y1 < y2):
                            return True
                    
                    # Check target-source vertical segments (if in same row)
                    if conn1['target_row'] == conn2['source_row']:
                        x1 = conn1['target_x']
                        x2 = conn2['source_x']
                        if (x1 < x2 and y1 > y2) or (x1 > x2 and y1 < y2):
                            return True
    
    # No vertical-vertical crossings found
    return False

def try_find_order_without_vertical_crossings(connection_groups):
    """
    Attempt to find an order without vertical crossings using the boundary affinity approach.
    
    Returns:
        A list of group IDs in an order that avoids vertical crossings, or None if not found
    """
    import itertools
    
    # Get group IDs
    group_ids = list(connection_groups.keys())
    
    # For small numbers of groups, we can try all permutations
    if len(group_ids) <= 6:  # 6! = 720 permutations
        for order in itertools.permutations(group_ids):
            if not has_vertical_vertical_crossings(order, connection_groups):
                return list(order)  # Found a valid order
    
    # For larger groups, try a sampling approach
    else:
        # First, try the boundary affinity sorting
        boundary_affinity = {}
        for group_id, connections in connection_groups.items():
            top_conns = sum(1 for c in connections if c['source_row'] == 0 or c['target_row'] == 0)
            bot_conns = sum(1 for c in connections if c['source_row'] == 1 or c['target_row'] == 1)
            
            # Groups with higher affinity to top row should be placed higher
            boundary_affinity[group_id] = top_conns - bot_conns
        
        # Sort groups by their boundary affinity
        ordered_groups = sorted(
            connection_groups.keys(),
            key=lambda g: boundary_affinity.get(g, 0),
            reverse=True  # Higher affinity to top comes first
        )
        
        # Check if this ordering works
        if not has_vertical_vertical_crossings(ordered_groups, connection_groups):
            return ordered_groups
        
        # If not, try random permutations
        import random
        attempts = min(500, 10 * len(group_ids)**2)  # Try more for larger problems
        
        for _ in range(attempts):
            # Start with the affinity-based order but shuffle it slightly
            test_order = ordered_groups.copy()
            
            # Choose two random positions and swap them
            i, j = random.sample(range(len(test_order)), 2)
            test_order[i], test_order[j] = test_order[j], test_order[i]
            
            # Check if this avoids vertical crossings
            if not has_vertical_vertical_crossings(test_order, connection_groups):
                return test_order
    
    # Couldn't find an order without vertical crossings
    return None

def optimize_connection_order(connection_groups):
    """
    Optimize the order of connection groups to minimize crossings.
    This function prioritizes eliminating vertical-vertical crossings.
    
    Args:
        connection_groups: Dictionary mapping group IDs to lists of connections
        
    Returns:
        Ordered list of group IDs
    """
    # Handle empty or single-group cases
    if not connection_groups:
        return []
    if len(connection_groups) <= 1:
        return list(connection_groups.keys())
    
    # First priority: Try to find an order without vertical crossings
    no_vertical_crossings_order = try_find_order_without_vertical_crossings(connection_groups)
    if no_vertical_crossings_order:
        return no_vertical_crossings_order
    
    # If we can't eliminate all vertical crossings, fall back to the original strategy
    # First strategy: Sort by boundary affinity (how much they connect to top vs. bottom)
    boundary_affinity = {}
    for group_id, connections in connection_groups.items():
        top_conns = sum(1 for c in connections if c['source_row'] == 0 or c['target_row'] == 0)
        bot_conns = sum(1 for c in connections if c['source_row'] == 1 or c['target_row'] == 1)
        
        # Groups with higher affinity to top row should be placed higher
        boundary_affinity[group_id] = top_conns - bot_conns
    
    # Sort groups by their boundary affinity
    ordered_groups = sorted(
        connection_groups.keys(),
        key=lambda g: boundary_affinity.get(g, 0),
        reverse=True  # Higher affinity to top comes first
    )
    
    # Second strategy: Consider crossing difficulty
    # Calculate difficulty scores
    difficulty = {group_id: estimate_crossing_difficulty(connections) 
                 for group_id, connections in connection_groups.items()}
    
    # Try swapping adjacent groups to reduce crossings
    improved = True
    max_iterations = 20  # Limit iterations to prevent infinite loop
    iteration = 0
    
    while improved and iteration < max_iterations:
        improved = False
        iteration += 1
        
        # Try swapping adjacent groups
        for i in range(len(ordered_groups) - 1):
            # Try swapping groups at positions i and i+1
            current_order = ordered_groups.copy()
            
            # Swap
            current_order[i], current_order[i+1] = current_order[i+1], current_order[i]
            
            # Check if this reduces crossings or eliminates vertical crossings
            if not has_vertical_vertical_crossings(current_order, connection_groups):
                # If this eliminates vertical crossings, use it immediately
                ordered_groups = current_order
                return ordered_groups
            elif difficulty[current_order[i]] > difficulty[current_order[i+1]]:
                # Update order based on difficulty
                ordered_groups = current_order
                improved = True
                break
    
    return ordered_groups

def assign_optimal_heights(connection_groups, middle_y, vertical_gap):
    """
    Assign optimal heights to connection groups to minimize crossings.
    
    Args:
        connection_groups: Dictionary mapping group IDs to lists of connections
        middle_y: Middle y-coordinate between rows
        vertical_gap: Vertical gap between rows
        
    Returns:
        Dictionary mapping group IDs to y-positions
    """
    # Get optimal ordering of groups
    ordered_groups = optimize_connection_order(connection_groups)
    
    # Calculate optimal heights based on order
    group_heights = {}
    
    # Calculate routing height available
    routing_height = (2.0/3.0) * vertical_gap
    
    # If we have groups, distribute them in the optimal order
    if ordered_groups:
        num_groups = len(ordered_groups)
        
        if num_groups == 1:
            # With only one group, use the middle
            group_heights[ordered_groups[0]] = middle_y
        else:
            # With multiple groups, distribute them evenly
            start_y = middle_y - routing_height/3
            end_y = middle_y + routing_height/3
            
            if num_groups > 1:
                step = (end_y - start_y) / (num_groups - 1)
                
                for i, group_id in enumerate(ordered_groups):
                    group_heights[group_id] = start_y + i * step
            else:
                # Fallback for one group
                group_heights[ordered_groups[0]] = middle_y
    
    return group_heights
