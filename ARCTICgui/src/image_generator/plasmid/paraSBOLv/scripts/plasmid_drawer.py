"""
Drawing utilities for plasmid visualization.
Contains functions for drawing constructs and connections.
"""
import image_generator.plasmid.paraSBOLv.parasbolv.parasbolv as psv
from image_generator.plasmid.paraSBOLv.scripts.plasmid_utils import parse_gene_info, create_gene_constructs, log
from image_generator.plasmid.paraSBOLv.scripts.plasmid_connection_router import ConnectionRouter

def calculate_line_width(ax, base_width=1.5):
    """
    Get line width for connections.
    
    Args:
        ax: Matplotlib axis (not used, kept for compatibility)
        base_width: Default line width to use
        
    Returns:
        Line width value to use for connection lines
    """
    return base_width

def draw_constructs(ax, row_data, row_index, start_y, spacing):
    """
    Draw all constructs for a row.
    
    Args:
        ax: Matplotlib axis to draw on
        row_data: List of gene strings for this row
        row_index: Index of this row (0 for top, 1 for bottom)
        start_y: Y coordinate for this row
        spacing: Horizontal spacing between constructs
        
    Returns:
        List of drawn construct information
    """
    renderer = psv.GlyphRenderer()
    drawn_constructs = []
    
    # Calculate total row width
    total_width = 0
    for i, gene_str in enumerate(row_data):
        total_width += 120  # Base width for each construct
        if i < len(row_data) - 1:
            total_width += spacing
    
    # Draw row backbone
    row_start_x = 10
    ax.plot([row_start_x, row_start_x + total_width], [start_y, start_y], 
            color=(0, 0, 0), linewidth=2.0, zorder=0)
    log(f"Row {row_index} backbone drawn at y={start_y}")
    
    current_x = row_start_x
    for i, gene_str in enumerate(row_data):
        # Parse gene information
        gene_info = parse_gene_info(gene_str)
        if not gene_info:
            continue
        
        # Create gene parts
        gene_constructs = create_gene_constructs([gene_info], row_index, i)
        if not gene_constructs:
            continue
        
        # Create and draw construct
        construct = psv.Construct(
            gene_constructs[0]['parts'],
            renderer,
            fig=ax.figure,
            ax=ax,
            start_position=(current_x, start_y),
            padding=5
        )
        fig, ax, baseline_start, baseline_end, bounds = construct.draw()
        
        # Add element name label - position above for top row, below for bottom row
        label_y_offset = 15 if row_index == 0 else -15  # Up for top row (0), down for bottom row (1)
        label_v_align = 'bottom' if row_index == 0 else 'top'
        
        # Use device name or CDS target as the element name
        from image_generator.plasmid.paraSBOLv.scripts.plasmid_utils  import get_device_label
        element_name = get_device_label(gene_info)
        
        # Position at center of construct
        label_x = (baseline_start[0] + baseline_end[0]) / 2
        
        ax.text(
            label_x,
            start_y + label_y_offset,
            element_name,
            fontsize=10,
            # fontweight='bold',
            ha='center',
            va=label_v_align
        )
        
        # Calculate and store part positions
        part_positions = []
        
        for j, part in enumerate(gene_constructs[0]['parts']):
            glyph_type = part.glyph_type
            
            # Calculate position based on part index
            part_width = (baseline_end[0] - baseline_start[0]) / len(gene_constructs[0]['parts'])
            part_x = baseline_start[0] + j * part_width
            part_y = baseline_start[1]
            
            # Adjust width for different part types
            width = part_width
            if glyph_type == 'CDS':
                width = 40
            elif glyph_type == 'Promoter':
                width = 15
                
                # Try to get the promoter source from gene info
                promoter_source = gene_info.get('promoter_source', '')
                
                # Get the corresponding input sensor name if this is an input promoter
                # Input promoters typically have single letter names (a, b, c)
                promoter_label = None
                
                # Import storage to access selected input sensors
                from data.data_storage import storage
                
                if len(promoter_source) == 1 and promoter_source.isalpha():
                    # This is an input promoter, use the selected input sensor name
                    if hasattr(storage, 'selected_input_sensors') and promoter_source in storage.selected_input_sensors:
                        promoter_label = storage.selected_input_sensors[promoter_source]
                    else:
                        promoter_label = f"Input {promoter_source.upper()}"
                
                # Add label only if we have one
                if promoter_label:
                    # Increase the y-offset to position labels higher above the promoter
                    # to avoid overlapping with the plasmid arrow
                    promoter_label_y_offset = 15  # Increased from 8 to 15 for better clearance
                    
                    # Add label text
                    ax.text(
                        part_x + width/2,  # Center over promoter
                        part_y + promoter_label_y_offset,  # Higher position above the promoter
                        promoter_label,
                        fontsize=7,        # Slightly smaller font
                        color=(0.3, 0.3, 0.3),  # Darker gray color
                        ha='center',
                        va='bottom',       # Align from bottom
                        bbox=dict(facecolor='white', alpha=0.7, pad=1, edgecolor='none')  # Add a semi-transparent white background
                    )
                
            elif glyph_type == 'Terminator':
                width = 10
            elif glyph_type == 'RibosomeEntrySite':
                width = 15
            
            part_info = {
                'part_type': glyph_type,
                'position': (part_x, part_y),
                'width': width,
                'index': j
            }
            part_positions.append(part_info)
        
        # Store construct information
        drawn_constructs.append({
            'gene_info': gene_info,
            'construct': construct,
            'bounds': bounds,
            'baseline': (baseline_start, baseline_end),
            'parts_positions': part_positions,
            'row_index': row_index,
            'gene_position': i
        })
        
        # Update current_x for next construct
        current_x = baseline_end[0] + spacing
        
    return drawn_constructs

def draw_connections(ax, connections_to_draw, drawn_constructs_by_row, vertical_gap):
    """
    Draw connections between elements based on row and position indices.
    
    Args:
        ax: Matplotlib axis to draw on
        connections_to_draw: List of connection definitions
        drawn_constructs_by_row: List of drawn constructs for each row
        vertical_gap: Vertical gap between rows
    """
    log("\nDrawing connections...")
    
    # Calculate appropriate line width for this figure
    line_width = calculate_line_width(ax)
    
    # Get middle area coordinate directly from row positions
    if (len(drawn_constructs_by_row) >= 2 and 
        len(drawn_constructs_by_row[0]) > 0 and 
        len(drawn_constructs_by_row[1]) > 0):
        
        # Get y position from first construct's baseline in each row
        top_row_y = drawn_constructs_by_row[0][0]['baseline'][0][1]
        bottom_row_y = drawn_constructs_by_row[1][0]['baseline'][0][1]
        
        # Calculate middle between rows
        mid_area_y = (top_row_y + bottom_row_y) / 2.0
        actual_gap = abs(top_row_y - bottom_row_y)
    else:
        # Fallback if no constructs are drawn
        mid_area_y = 140
        actual_gap = vertical_gap
    
    # Create connection router
    router = ConnectionRouter(mid_area_y, actual_gap)
    
    # Group connections by their group ID
    connections_by_group = router.group_connections(connections_to_draw)
    
    # Process groups to ensure distinct heights
    group_infos = router.process_connection_groups(connections_by_group, drawn_constructs_by_row, mid_area_y)
    
    # Draw each group
    for group_info in group_infos:
        # Add line width to group info for drawing functions
        group_info["line_width"] = line_width
        
        # Draw connections using the router-calculated positions
        if group_info["type"] == "single":
            _draw_single_connection(ax, group_info)
        elif group_info["type"] == "fan_in":
            _draw_fan_in_connection(ax, group_info)
        elif group_info["type"] == "fan_out":
            _draw_fan_out_connection(ax, group_info)
        else:  # "complex"
            _draw_complex_connection(ax, group_info)

def _draw_single_connection(ax, group_info):
    """
    Draw a single connection (one source to one target).
    
    Args:
        ax: Matplotlib axis to draw on
        group_info: Dictionary with connection information
    """
    conn = group_info["connections"][0]
    conn_id = conn.get('id')  # Use .get() to handle missing keys
    
    positions = group_info["positions"]
    if conn_id not in positions:
        return
    
    pos_info = positions[conn_id]
    source_pos = pos_info['source']
    target_pos = pos_info['target']
    group_color = group_info["color"]
    group_y = group_info["y_pos"]
    line_width = group_info.get("line_width", 2.0)
    
    log(f"Drawing single connection for group {group_info['group_id']} at y={group_y}")
    log(f"  - Connection from {source_pos} to {target_pos}")
    
    # Draw the vertical segment from source to group_y
    ax.plot(
        [source_pos[0], source_pos[0]], 
        [source_pos[1], group_y],
        color=group_color, linewidth=line_width, zorder=1
    )
    
    # Draw the horizontal segment
    ax.plot(
        [source_pos[0], target_pos[0]], 
        [group_y, group_y],
        color=group_color, linewidth=line_width, zorder=1
    )
    
    # Draw the vertical segment to the target
    ax.plot(
        [target_pos[0], target_pos[0]], 
        [group_y, target_pos[1]],
        color=group_color, linewidth=line_width, zorder=1
    )
    
    # Draw hash mark at target
    hash_size = 3
    ax.plot(
        [target_pos[0] - hash_size, target_pos[0] + hash_size], 
        [target_pos[1], target_pos[1]],
        color=group_color, linewidth=line_width, zorder=1
    )

def _draw_fan_in_connection(ax, group_info):
    """
    Draw a fan-in connection (multiple sources to one target).
    This draws connections from multiple sources that converge to a single target.
    
    Args:
        ax: Matplotlib axis to draw on
        group_info: Dictionary with connection information
    """
    positions = group_info["positions"]
    group_color = group_info["color"]
    group_y = group_info["y_pos"]
    line_width = group_info.get("line_width", 2.0)
    
    # Get all source positions and the common target
    source_positions = []
    target_pos = None
    
    log(f"Drawing fan-in connection for group {group_info['group_id']} at y={group_y}")
    
    for conn in group_info["connections"]:
        conn_id = conn.get('id')  # Use .get() to handle missing keys
        if conn_id and conn_id in positions:
            source_positions.append(positions[conn_id]['source'])
            if not target_pos:
                target_pos = positions[conn_id]['target']
    
    if not source_positions or not target_pos:
        log(f"Warning: Missing source or target positions for group {group_info['group_id']}")
        return
    
    # Draw vertical segments from all sources
    for source_pos in source_positions:
        ax.plot(
            [source_pos[0], source_pos[0]], 
            [source_pos[1], group_y],
            color=group_color, linewidth=line_width, zorder=1
        )
    
    # Find the x-range to span all sources
    min_x = min(pos[0] for pos in source_positions)
    max_x = max(pos[0] for pos in source_positions)
    
    # Draw horizontal segments that connect ALL sources to the target
    # First, draw horizontal segment spanning all sources
    if len(source_positions) > 1:
        ax.plot(
            [min_x, max_x],
            [group_y, group_y],
            color=group_color, linewidth=line_width, zorder=1
        )
    
    # Now connect this segment to the target if target is outside the source span
    if target_pos[0] < min_x:
        # Target is to the left of all sources
        ax.plot(
            [target_pos[0], min_x],
            [group_y, group_y],
            color=group_color, linewidth=line_width, zorder=1
        )
    elif target_pos[0] > max_x:
        # Target is to the right of all sources
        ax.plot(
            [max_x, target_pos[0]],
            [group_y, group_y],
            color=group_color, linewidth=line_width, zorder=1
        )
    
    # Draw the vertical segment to the target
    ax.plot(
        [target_pos[0], target_pos[0]], 
        [group_y, target_pos[1]],
        color=group_color, linewidth=line_width, zorder=1
    )
    
    # Draw hash mark at target
    hash_size = 3
    ax.plot(
        [target_pos[0] - hash_size, target_pos[0] + hash_size], 
        [target_pos[1], target_pos[1]],
        color=group_color, linewidth=line_width, zorder=1
    )

def _draw_fan_out_connection(ax, group_info):
    """
    Draw a fan-out connection (one source to multiple targets).
    This draws connections from a single source that branch out to multiple targets.
    
    Args:
        ax: Matplotlib axis to draw on
        group_info: Dictionary with connection information
    """
    positions = group_info["positions"]
    group_color = group_info["color"]
    group_y = group_info["y_pos"]
    line_width = group_info.get("line_width", 2.0)
    
    # Get the common source and all target positions
    source_pos = None
    target_positions = []
    
    log(f"Drawing fan-out connection for group {group_info['group_id']} at y={group_y}")
    
    for conn in group_info["connections"]:
        conn_id = conn.get('id')
        if conn_id and conn_id in positions:
            target_positions.append(positions[conn_id]['target'])
            if not source_pos:
                source_pos = positions[conn_id]['source']
    
    if not source_pos or not target_positions:
        log(f"Warning: Missing source or target positions for group {group_info['group_id']}")
        return
    
    # Find the x-range for all targets
    min_target_x = min(pos[0] for pos in target_positions)
    max_target_x = max(pos[0] for pos in target_positions)
    
    # Draw vertical segment from source
    ax.plot(
        [source_pos[0], source_pos[0]], 
        [source_pos[1], group_y],
        color=group_color, linewidth=line_width, zorder=1
    )
    
    # Draw horizontal segments based on source and target positions
    if min_target_x < source_pos[0] and max_target_x > source_pos[0]:
        # Source is between targets - draw two horizontal segments
        
        # First segment to targets on the left
        ax.plot(
            [min_target_x, source_pos[0]], 
            [group_y, group_y],
            color=group_color, linewidth=line_width, zorder=1
        )
        
        # Second segment to targets on the right
        ax.plot(
            [source_pos[0], max_target_x], 
            [group_y, group_y],
            color=group_color, linewidth=line_width, zorder=1
        )
    else:
        # Source is at one end - draw one horizontal segment
        horizontal_range = [min_target_x, max_target_x]
        
        # If source is to the left of all targets
        if source_pos[0] < min_target_x:
            horizontal_range[0] = source_pos[0]
        # If source is to the right of all targets
        elif source_pos[0] > max_target_x:
            horizontal_range[1] = source_pos[0]
        
        # Draw the horizontal segment
        ax.plot(
            horizontal_range,
            [group_y, group_y],
            color=group_color, linewidth=line_width, zorder=1
        )
    
    # Draw vertical segments to all targets
    for target_pos in target_positions:
        ax.plot(
            [target_pos[0], target_pos[0]], 
            [group_y, target_pos[1]],
            color=group_color, linewidth=line_width, zorder=1
        )
        
        # Draw hash mark at target
        hash_size = 3
        ax.plot(
            [target_pos[0] - hash_size, target_pos[0] + hash_size], 
            [target_pos[1], target_pos[1]],
            color=group_color, linewidth=line_width, zorder=1
        )

def _draw_complex_connection(ax, group_info):
    """
    Draw a complex connection (multiple sources to multiple targets).
    This handles cases where the connection pattern doesn't fit the simpler categories.
    
    Args:
        ax: Matplotlib axis to draw on
        group_info: Dictionary with connection information
    """
    positions = group_info["positions"]
    group_color = group_info["color"]
    group_y = group_info["y_pos"]
    line_width = group_info.get("line_width", 2.0)
    
    log(f"Drawing complex connection for group {group_info['group_id']} at y={group_y}")
    
    # Get all source and target positions
    valid_connections = []
    
    for conn in group_info["connections"]:
        conn_id = conn.get('id')
        if conn_id and conn_id in positions:
            valid_connections.append({
                'id': conn_id,
                'source': positions[conn_id]['source'],
                'target': positions[conn_id]['target']
            })
    
    if not valid_connections:
        log(f"Warning: No valid connections for group {group_info['group_id']}")
        return
        
    # Draw all connections individually
    for conn in valid_connections:
        source_pos = conn['source']
        target_pos = conn['target']
        
        # Draw the vertical segment from source to group_y
        ax.plot(
            [source_pos[0], source_pos[0]], 
            [source_pos[1], group_y],
            color=group_color, linewidth=line_width, zorder=1
        )
        
        # Draw the horizontal segment
        ax.plot(
            [source_pos[0], target_pos[0]], 
            [group_y, group_y],
            color=group_color, linewidth=line_width, zorder=1
        )
        
        # Draw the vertical segment to the target
        ax.plot(
            [target_pos[0], target_pos[0]], 
            [group_y, target_pos[1]],
            color=group_color, linewidth=line_width, zorder=1
        )
        
        # Draw hash mark at target
        hash_size = 3
        ax.plot(
            [target_pos[0] - hash_size, target_pos[0] + hash_size], 
            [target_pos[1], target_pos[1]],
            color=group_color, linewidth=line_width, zorder=1
        )