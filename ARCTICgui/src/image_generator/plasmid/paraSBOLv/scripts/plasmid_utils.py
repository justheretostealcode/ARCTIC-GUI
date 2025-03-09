"""
Utility functions for plasmid diagram generation.
Contains parsing, color mapping, and generic helper functions.
"""
import re
from collections import namedtuple

# Enable/disable debug output
DEBUG = False

def log(message):
    """Print debug messages only if DEBUG is enabled"""
    if DEBUG:
        print(message)


# Define the Part namedtuple
Part = namedtuple('part', ['glyph_type', 'orientation', 'user_parameters', 'style_parameters'])

# Colors for each element in the top and bottom rows
ELEMENT_COLORS_BY_ROW = {
    0: [  # top row
        (1.0, 0.7, 0.7),  # pink
        (0.0, 0.0, 1.0),  # blue
        (1.0, 0.5, 0.0),  # orange
        (1.0, 0.5, 0.0),  # orange
        (0.0, 1.0, 0.0)   # green
    ],
    1: [  # bottom row
        (0.0, 1.0, 0.0),  # green
        (1.0, 0.7, 0.7),  # pink
        (1.0, 0.0, 0.0),  # red
        (0.0, 0.0, 1.0)   # blue
    ]
}

def parse_gene_info(gene_str):
    """
    Parse gene information from a gene string.
    Returns a dictionary with extracted information.
    """
    # Extract gene number and basic info
    gene_match = re.match(r'Gene (\d+) \((P (.*?) -> CDS (.*?))\): (.*)', gene_str)
    if not gene_match:
        return None
    
    gene_num = gene_match.group(1)
    gene_expression = gene_match.group(2)
    promoter_source = gene_match.group(3)
    cds_target = gene_match.group(4)
    details = gene_match.group(5)
    
    # Parse detailed components
    components = {}
    for component in details.split(' '):
        if '=' in component:
            key, value = component.split('=', 1)
            components[key] = value
    
    # Extract protein/device name from CDS component
    device_name = None
    if 'CDS' in components:
        device_name = components['CDS'].replace('protein_', '')
    
    return {
        'gene_num': gene_num,
        'gene_expression': gene_expression,
        'promoter_source': promoter_source,
        'cds_target': cds_target,
        'components': components,
        'device_name': device_name,
        'raw_string': gene_str
    }

def get_element_color(row_index, position_index):
    """Get color for an element based on its row and position"""
    if row_index in ELEMENT_COLORS_BY_ROW:
        color_list = ELEMENT_COLORS_BY_ROW[row_index]
        if position_index < len(color_list):
            return color_list[position_index]
        else:
            # Use the last available color if position exceeds list length
            return color_list[-1]
    
    # Default fallback - gray
    return (0.5, 0.5, 0.5)

def create_gene_constructs(parsed_genes, row_index, gene_position):
    """Create construct parts from parsed gene information."""
    gene_constructs = []
    
    for gene_info in parsed_genes:
        parts = []
        
        # Get color based on row and position
        color = get_element_color(row_index, gene_position)
        
        # Create promoter part
        promoter_style = None  # Let parasbolv use default style
        parts.append(Part('Promoter', 'forward', None, promoter_style))
        
        # Create RBS part if specified
        if gene_info['components'].get('UTR'):
            rbs_style = None
            parts.append(Part('RibosomeEntrySite', 'forward', None, rbs_style))
        
        # Create CDS part
        cds_style = {
            'cds': {
                'facecolor': color,
                'edgecolor': (0, 0, 0),
                'linewidth': 1.5
            }
        }
        parts.append(Part('CDS', 'forward', {'width': 40}, cds_style))
        
        # Always add terminator part
        terminator_style = None
        parts.append(Part('Terminator', 'forward', None, terminator_style))
        
        gene_constructs.append({
            'parts': parts,
            'info': gene_info
        })
    
    return gene_constructs

def check_segments_overlap(seg1, seg2):
    """Check if two horizontal segments overlap"""
    # Different y positions means no overlap
    if seg1['y_pos'] != seg2['y_pos']:
        return False
        
    # Same source-target pair or color should overlap (intentional)
    if (seg1['source_key'] == seg2['source_key'] and 
        seg1['target_key'] == seg2['target_key']):
        return False
        
    # Same color connections should be allowed to overlap
    if seg1['color'] == seg2['color']:
        return False
    
    # Check x-coordinate overlap
    x1_min = min(seg1['x1'], seg1['x2'])
    x1_max = max(seg1['x1'], seg1['x2'])
    x2_min = min(seg2['x1'], seg2['x2'])
    x2_max = max(seg2['x1'], seg2['x2'])
    
    # If one segment ends before the other begins, no overlap
    if x1_max < x2_min or x2_max < x1_min:
        return False
        
    return True  # Segments overlap

def generate_connections_from_plasmid_data(plasmid_data):
    """
    Generate connection definitions by directly using the relationships
    encoded in the plasmid data (P source -> CDS target relationships).
    
    Args:
        plasmid_data: List of gene strings for each row
        
    Returns:
        List of connection definitions for drawing
    """
    log("\nGenerating connections directly from local plasmid data .py file (not hehe)")
    
    # Step 1: Map all elements to their positions
    cds_to_positions = {}  # Maps CDS ID to position(s)
    position_to_cds = {}   # Maps position to CDS ID
    
    # Map all CDS elements with their positions
    for row_idx, row_data in enumerate(plasmid_data):
        for pos_idx, gene_str in enumerate(row_data):
            if gene_str is None:
                continue
                
            gene_info = parse_gene_info(gene_str)
            if gene_info:
                cds_id = gene_info['cds_target']
                position = (row_idx, pos_idx)
                
                # Store position of this CDS
                position_to_cds[position] = cds_id
                if cds_id not in cds_to_positions:
                    cds_to_positions[cds_id] = []
                cds_to_positions[cds_id].append(position)
                
                log(f"  CDS {cds_id} at position ({row_idx}, {pos_idx})")
    
    # Step 2: Track actual promoter->target relationships
    direct_connections = []
    
    # Maps target positions to their source positions
    # target_pos -> [(source_pos, promoter_id), ...]
    target_to_sources = {}
    
    log("\nAnalyzing gene relationships:")
    for row_idx, row_data in enumerate(plasmid_data):
        for pos_idx, gene_str in enumerate(row_data):
            if gene_str is None:
                continue
                
            gene_info = parse_gene_info(gene_str)
            if not gene_info:
                continue
                
            promoter_id = gene_info['promoter_source']
            target_id = gene_info['cds_target']
            target_pos = (row_idx, pos_idx)
            
            log(f"  Analyzing gene at {target_pos}: {promoter_id} -> {target_id}")
            
            # Skip inputs (a, b, c)
            if len(promoter_id) == 1 and promoter_id.isalpha():
                log(f"    Input promoter: {promoter_id}")
                continue
            
            # Find the positions of elements with this promoter ID
            source_positions = cds_to_positions.get(promoter_id, [])
            
            if source_positions:
                # Store this direct relationship
                if target_pos not in target_to_sources:
                    target_to_sources[target_pos] = []
                    
                for source_pos in source_positions:
                    target_to_sources[target_pos].append((source_pos, promoter_id))
                    
                    # Add to direct connections
                    direct_connections.append({
                        "source": source_pos,
                        "target": target_pos,
                        "source_id": promoter_id,
                        "target_id": target_id
                    })
    
    # Step 3: Group connections by target type to match expected output
    log("\nGrouping connections by target type:")
    
    # Group connections by target CDS type
    target_groups = {}  # Maps target CDS type to list of connections
    
    for connection in direct_connections:
        target_pos = connection["target"]
        target_id = position_to_cds.get(target_pos)
        
        if target_id not in target_groups:
            target_groups[target_id] = []
            
        target_groups[target_id].append(connection)
    
    # Special case for NOT_1 - group its outgoing connections separately
    not1_connections = []
    for connection in direct_connections:
        source_pos = connection["source"]
        if position_to_cds.get(source_pos) == "NOT_1":
            not1_connections.append(connection)
    
    # Remove NOT_1 outgoing connections from their target groups to create a separate group
    if not1_connections:
        for connection in not1_connections:
            target_id = position_to_cds.get(connection["target"])
            if target_id in target_groups:
                target_groups[target_id] = [c for c in target_groups[target_id] if c["source"] != connection["source"]]
                
                # Remove empty groups
                if not target_groups[target_id]:
                    del target_groups[target_id]
    
    # Step 4: Create final connection groups with IDs
    grouped_connections = []  # List of connections with group IDs
    next_group_id = 1
    
    # Process regular target groups
    log("\nFinal connection groups:")
    for target_id, connections in target_groups.items():
        if connections:  # Skip empty groups
            group_id = next_group_id
            next_group_id += 1
            
            log(f"  Group {group_id}: Target {target_id}")
            for conn in connections:
                source_pos = conn["source"]
                target_pos = conn["target"]
                source_id = position_to_cds.get(source_pos, "Unknown")
                
                connection = {
                    "id": str(len(grouped_connections) + 1),
                    "source_row": source_pos[0],
                    "source_pos": source_pos[1],
                    "target_row": target_pos[0],
                    "target_pos": target_pos[1],
                    "source_id": source_id,
                    "target_id": target_id,
                    "group": str(group_id)
                }
                grouped_connections.append(connection)
                log(f"    - ({source_pos[0]},{source_pos[1]}) → ({target_pos[0]},{target_pos[1]}) [{source_id} → {target_id}]")
    
    # Add NOT_1 group if it exists
    if not1_connections:
        not1_group_id = next_group_id
        next_group_id += 1
        
        log(f"  Group {not1_group_id}: Source NOT_1")
        for conn in not1_connections:
            source_pos = conn["source"]
            target_pos = conn["target"]
            target_id = position_to_cds.get(target_pos, "Unknown")
            
            connection = {
                "id": str(len(grouped_connections) + 1),
                "source_row": source_pos[0],
                "source_pos": source_pos[1],
                "target_row": target_pos[0],
                "target_pos": target_pos[1],
                "source_id": "NOT_1",
                "target_id": target_id,
                "group": str(not1_group_id)
            }
            grouped_connections.append(connection)
            log(f"    - ({source_pos[0]},{source_pos[1]}) → ({target_pos[0]},{target_pos[1]}) [NOT_1 → {target_id}]")
    
    log(f"\nGenerated {len(grouped_connections)} connections in {next_group_id-1} groups")
    return grouped_connections

def get_device_label(gene_info):
    """
    Extract a descriptive label from gene info.
    Prefers the device/protein name over the CDS target ID.
    
    Args:
        gene_info: Dictionary with gene information
    
    Returns:
        String label for the gene
    """
    if not gene_info:
        return "Unknown"
        
    # First try to get device name
    if gene_info.get('device_name'):
        return gene_info['device_name']
    
    # Fall back to CDS target
    if gene_info.get('cds_target'):
        return gene_info['cds_target']
    
    # Last resort
    return "Gene"
