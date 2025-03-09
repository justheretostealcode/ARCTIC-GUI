"""
Connection routing algorithms for plasmid diagrams.
Handles routing of connections between elements.
"""
from plasmid_utils import check_segments_overlap, get_element_color, log
from plasmid_crossings_minimizer import optimize_connection_order

class ConnectionRouter:
    """Routes connections between genetic elements in plasmid diagrams"""
    
    def __init__(self, middle_area_y=50, vertical_gap=70):
        """
        Initialize the connection router
        
        Args:
            middle_area_y: Y-coordinate of the middle area between rows
            vertical_gap: Vertical gap between rows (affects routing space)
        """
        self.middle_area_y = middle_area_y
        self.vertical_gap = vertical_gap
        
        # Constants for vertical offsets from elements
        self.VERTICAL_OFFSET_TOP = 10     
        self.VERTICAL_OFFSET_BOTTOM = 20

    def calculate_positions(self, connections, drawn_constructs_by_row):
        """
        Calculate all source and target positions for connections
        
        Returns:
            Dictionary mapping connection IDs to their positions
        """
        connection_positions = {}
        horizontal_segments = []
        color_by_source = {}
        
        # Build color mapping
        for connection in connections:
            source_row = connection['source_row']
            source_pos = connection['source_pos']
            source_key = f"{source_row}_{source_pos}"
            
            # Get color from drawn construct
            if (source_row < len(drawn_constructs_by_row) and
                source_pos < len(drawn_constructs_by_row[source_row])):
                construct = drawn_constructs_by_row[source_row][source_pos]
                
                # Find CDS part and get its color
                for part in construct['parts_positions']:
                    if part['part_type'] == 'CDS':
                        # Get color from CDS part style
                        for original_part in construct['construct'].part_list:
                            if original_part.glyph_type == 'CDS':
                                if original_part.style_parameters and 'cds' in original_part.style_parameters:
                                    if 'facecolor' in original_part.style_parameters['cds']:
                                        color_by_source[source_key] = original_part.style_parameters['cds']['facecolor']
                                        break
                        
                        # If color not found, use row/position-based color
                        if source_key not in color_by_source:
                            color_by_source[source_key] = get_element_color(source_row, source_pos)
                        break
                
                # Fallback if no CDS part found
                if source_key not in color_by_source:
                    color_by_source[source_key] = get_element_color(source_row, source_pos)
        
        # Calculate positions for each connection
        for connection in connections:
            conn_id = connection['id']
            source_row = connection['source_row']
            source_pos = connection['source_pos']
            target_row = connection['target_row']
            target_pos = connection['target_pos']
            
            # Skip if source or target out of range
            if (source_row >= len(drawn_constructs_by_row) or 
                source_pos >= len(drawn_constructs_by_row[source_row]) or
                target_row >= len(drawn_constructs_by_row) or 
                target_pos >= len(drawn_constructs_by_row[target_row])):
                continue
            
            # Get source and target constructs
            source_construct = drawn_constructs_by_row[source_row][source_pos]
            target_construct = drawn_constructs_by_row[target_row][target_pos]
            
            # Source position (center of CDS)
            source_position = None
            for part in source_construct['parts_positions']:
                if part['part_type'] == 'CDS':
                    x = part['position'][0] + part['width'] / 2
                    y = part['position'][1]
                    
                    # For top row: Add NEGATIVE offset to go DOWN
                    # For bottom row: Add POSITIVE offset to go UP
                    vertical_offset = self.VERTICAL_OFFSET_TOP if source_row == 0 else self.VERTICAL_OFFSET_BOTTOM
                    source_position = (x, y + (-vertical_offset if source_row == 0 else vertical_offset))
                    break
            
            # Target position (at promoter)
            target_position = None
            for part in target_construct['parts_positions']:
                if part['part_type'] == 'Promoter':
                    x = part['position'][0]
                    y = part['position'][1]
                    
                    vertical_offset = self.VERTICAL_OFFSET_TOP if target_row == 0 else self.VERTICAL_OFFSET_BOTTOM
                    target_position = (x, y + (-vertical_offset if target_row == 0 else vertical_offset))
                    break
            
            # Skip if positions not found
            if not source_position or not target_position:
                continue
            
            # Store positions
            source_key = f"{source_row}_{source_pos}"
            target_key = f"{target_row}_{target_pos}"
            
            connection_positions[conn_id] = {
                'source': source_position,
                'target': target_position,
                'source_key': source_key,
                'target_key': target_key
            }
            
            # Get color for this source
            source_color = color_by_source.get(source_key, (0.5, 0.5, 0.5))
            
            # Add to horizontal segments list
            horizontal_segments.append({
                'id': conn_id,
                'x1': source_position[0],
                'x2': target_position[0],
                'color': source_color,
                'source_key': source_key,
                'target_key': target_key,
                'y_pos': None  # Will be assigned later
            })
        
        return connection_positions, horizontal_segments, color_by_source
    
    def group_connections(self, connections):
        """
        Group connections by their group ID for multi-edge routing
        
        Args:
            connections: List of connection definitions
            
        Returns:
            Dictionary mapping group IDs to lists of connections
        """
        connections_by_group = {}
        for connection in connections:
            # Use group if available, otherwise use ID as a single-connection group
            group_id = connection.get('group', connection['id'])
            
            if group_id not in connections_by_group:
                connections_by_group[group_id] = []
            connections_by_group[group_id].append(connection)
            
        return connections_by_group
    
    def process_connection_groups(self, connections_by_group, drawn_constructs, mid_area_y):
        """
        Process ALL connection groups at once to ensure distinct heights.
        
        Args:
            connections_by_group: Dictionary mapping group IDs to lists of connections
            drawn_constructs: List of drawn constructs by row
            mid_area_y: Y-coordinate of the middle routing area
            
        Returns:
            List of group info dictionaries with position and drawing information
        """
        # First, calculate positions for ALL connections across ALL groups
        all_connection_positions = {}
        all_horizontal_segments = []
        all_color_by_source = {}
        
        # Gather unique group colors to assign distinct heights
        group_colors = {}  # Maps group ID to representative color
        
        # Process each group to calculate positions and gather info
        for group_id, connections in connections_by_group.items():
            # Calculate positions for this group
            connection_positions, horizontal_segments, color_by_source = self.calculate_positions(
                connections, drawn_constructs
            )
            
            # Skip empty groups
            if not connection_positions:
                continue
                
            # Find a representative connection to get color
            rep_conn = next((conn for conn in connections if conn['id'] in connection_positions), None)
            if not rep_conn:
                continue
                
            source_key = f"{rep_conn['source_row']}_{rep_conn['source_pos']}"
            group_color = color_by_source.get(source_key, (0.5, 0.5, 0.5))
            
            # Add connection source and target x-coordinates for crossing minimization
            enriched_connections = []
            for conn in connections:
                conn_id = conn['id']
                if conn_id in connection_positions:
                    source_x = connection_positions[conn_id]['source'][0]
                    target_x = connection_positions[conn_id]['target'][0]
                    
                    # Create copy with x-coordinates for the minimizer
                    enriched_conn = conn.copy()
                    enriched_conn['source_x'] = source_x
                    enriched_conn['target_x'] = target_x
                    enriched_connections.append(enriched_conn)
            
            # Store enriched connections for crossing minimization
            connections_by_group[group_id] = enriched_connections
            
            # Store color for this group
            group_colors[group_id] = group_color
            
            # Store connection positions
            all_connection_positions.update(connection_positions)
            all_horizontal_segments.extend(horizontal_segments)
            all_color_by_source.update(color_by_source)
            
        # Get optimized group order - pass drawn_constructs to use position information
        ordered_groups = optimize_connection_order(connections_by_group)
        
        # Calculate distinct y-levels for all groups
        routing_height = (2.0/3.0) * self.vertical_gap
        num_groups = len(group_colors)
        
        # Create more space between horizontal lines and elements
        virtual_num_groups = num_groups + (1 - num_groups % 2)  # Add padding, ensure odd number
        
        # Create y-levels for each group using the optimized order
        if num_groups <= 1:
            # With only one group, use the middle
            y_levels_by_group = {list(group_colors.keys())[0]: mid_area_y} if group_colors else {}
        else:
            # With multiple groups, distribute them evenly based on the optimized order
            start_y = mid_area_y - routing_height / 3
            end_y = mid_area_y + routing_height / 2 # Elements are located above the row backbone line
            
            # Create more positions than we need, then use only the middle ones
            y_levels = []
            
            if virtual_num_groups > 1:
                step = (end_y - start_y) / (virtual_num_groups - 1)
                for i in range(virtual_num_groups):
                    y_levels.append(start_y + i * step)
                    
                # Take the central positions (skip the first and last few)
                skip_count = (virtual_num_groups - num_groups) // 2
                y_levels = y_levels[skip_count:skip_count+num_groups]
            else:
                y_levels = [mid_area_y]
            
            # Assign levels to groups
            y_levels_by_group = {}
            for idx, group_id in enumerate(ordered_groups):
                if idx < len(y_levels):
                    y_levels_by_group[group_id] = y_levels[idx]
                else:
                    # Fallback if we somehow have more groups than levels
                    y_levels_by_group[group_id] = mid_area_y
        
        # Now, process each group with its assigned height
        group_infos = []
        
        for group_id, connections in connections_by_group.items():
            # Skip groups without a height assignment
            if group_id not in y_levels_by_group:
                continue
                
            # Get positions for this group's connections only
            group_positions = {conn.get('id', f"conn_{i}"): all_connection_positions.get(conn.get('id', f"conn_{i}"), None) 
                              for i, conn in enumerate(connections) 
                              if conn.get('id', f"conn_{i}") in all_connection_positions}
            
            # Try to match connections if ID doesn't match exactly
            if not group_positions:
                # Match by source and target positions
                for i, conn in enumerate(connections):
                    source_key = f"{conn['source_row']}_{conn['source_pos']}"
                    target_key = f"{conn['target_row']}_{conn['target_pos']}"
                    
                    # Check if we already have positions for this source-target pair
                    for conn_id, position in all_connection_positions.items():
                        if position['source_key'] == source_key and position['target_key'] == target_key:
                            group_positions[conn_id] = position
                            # Add a new id to the connection to match
                            conn['id'] = conn_id
                            break
            
            # Skip if there are still no valid positions
            if not group_positions:
                continue
                
            # Find a representative connection for this group
            rep_conn = next((conn for conn in connections if conn.get('id') in group_positions), None)
            if not rep_conn:
                continue
            
            source_key = f"{rep_conn['source_row']}_{rep_conn['source_pos']}"
            group_color = all_color_by_source.get(source_key, (0.5, 0.5, 0.5))
            
            # Determine connection type
            # Count unique sources and targets
            source_keys = set()
            target_keys = set()
            
            for conn in connections:
                source_key = f"{conn['source_row']}_{conn['source_pos']}"
                target_key = f"{conn['target_row']}_{conn['target_pos']}"
                source_keys.add(source_key)
                target_keys.add(target_key)
            
            # Determine connection type based on source/target counts
            if len(connections) == 1:
                connection_type = "single"
            elif len(source_keys) == 1 and len(target_keys) > 1:
                connection_type = "fan_out"  # One source to multiple targets
            elif len(source_keys) > 1 and len(target_keys) == 1:
                connection_type = "fan_in"  # Multiple sources to one target
            else:
                connection_type = "complex"
            
            # Use the pre-assigned height for this group
            group_y = y_levels_by_group[group_id]
            
            # Create group info
            group_info = {
                "group_id": group_id,
                "connections": connections,
                "positions": group_positions,
                "color": group_color,
                "y_pos": group_y,
                "type": connection_type
            }
            
            group_infos.append(group_info)
        
        # Order group_infos by y-position for better drawing order
        group_infos.sort(key=lambda g: g["y_pos"])
        
        return group_infos
