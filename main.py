import cv2
import numpy as np
import utils  # Make sure your utils file defines detect_horizontal_lines, detect_vertical_lines, detect_circles

def process_sections(img):
    """
    Process the full image by dividing it into sections,
    detecting horizontal and vertical lines and circles in each section,
    and computing a score for each circle (based on the column number).
    
    Input:
      img: the input image.
      
    Returns:
      results: a dictionary where each key is a section name and the value is
               another dict containing:
                 - "unique_cells": the unique circles detected (per cell)
                 - "row_scores": a dict mapping row number to its score (for display)
                 - "total_score": total score for that section
                 - "total_columns": number of columns (for computing scores)
                 - "output": the processed section image with circles drawn
    """
    # Resize image
    resized = cv2.resize(img, (800, 1000))
    
    # Define sections dictionary; each section is processed independently.
    sections = {
        "Section 1": resized[222:352, 530:750],
        "Section 2": resized[365:513, 535:743],
        "Section 3": resized[529:690, 535:743],
        "Section 4": resized[705:870, 535:743],
    }
    
    # Mapping of internal section names to the titles for printing
    section_titles = {
        "Section 1": "Commitment",
        "Section 2": "Knowledge of Subject",
        "Section 3": "Teaching for Independent Learning",
        "Section 4": "Management of Learning"
    }
    
    # Mapping of section to its questions per row.
    # Update these texts as needed.
    section_questions = {
        "Section 1": {
            1: "demonstrate sensitivity to students' ability to attend and absorb content information",
            2: "exhibit readiness and enthusiasm for professional development",
            3: "display consistency in teaching methodology",
            4: "adapt teaching to meet student needs",
            5: "engage students with diverse learning styles"
        },
        "Section 2": {
            1: "present subject matter with clarity",
            2: "use relevant examples and explanations",
            3: "integrate current research into teaching",
            4: "demonstrate mastery of core content",
            5: "address questions effectively"
        },
        "Section 3": {
            1: "encourage independent inquiry",
            2: "provide effective feedback",
            3: "support collaborative learning",
            4: "promote critical thinking",
            5: "use technology to enhance learning"
        },
        "Section 4": {
            1: "organize classroom effectively",
            2: "manage time efficiently",
            3: "set clear learning objectives",
            4: "maintain a positive classroom climate",
            5: "evaluate student progress fairly"
        }
    }
    
    results = {}
    
    for sec_name, sec_img in sections.items():
        print(f"\nProcessing {sec_name}:")
        
        # Detect horizontal lines to get row boundaries.
        output_h, y_coords = utils.detect_horizontal_lines(sec_img, section_name=sec_name)
        
        # Compute row ranges based on filtered y-coordinates.
        rows = []
        for i in range(len(y_coords) - 1):
            row_range = (int(y_coords[i]), int(y_coords[i+1]))
            rows.append(row_range)
        
        # Detect vertical lines to get column boundaries.
        output_v, x_coords = utils.detect_vertical_lines(sec_img, section_name=sec_name)
        
        # Compute column ranges from filtered x-coordinates.
        columns = []
        for i in range(len(x_coords) - 1):
            col_range = (int(x_coords[i]), int(x_coords[i+1]))
            columns.append(col_range)
        
        # Detect circles in the section.
        output_c, circles = utils.detect_circles(sec_img, section_name=sec_name)
        
        # For each detected circle, determine which column and row it falls into.
        circle_assignments = []
        for (x, y, r) in circles:
            col_assigned = None
            row_assigned = None
            
            # Determine column based on x-coordinate.
            for idx, (start, end) in enumerate(columns):
                if start <= x < end:
                    col_assigned = idx + 1  # Columns numbered starting at 1
                    break
            
            # Determine row based on y-coordinate.
            for idx, (start, end) in enumerate(rows):
                if start <= y < end:
                    row_assigned = idx + 1  # Rows numbered starting at 1
                    break
            
            if col_assigned is not None and row_assigned is not None:
                circle_assignments.append((row_assigned, col_assigned, x, y, r))
            else:
                print(f"{sec_name} - Circle at ({x}, {y}) did not fall within a proper cell range.")
        
        # Sort assignments by row then by column.
        circle_assignments.sort(key=lambda item: (item[0], item[1]))
        
        # Filter out duplicate circles in the same cell (only one per cell).
        unique_cells = {}
        for (row, col, x, y, r) in circle_assignments:
            cell_key = (row, col)
            if cell_key not in unique_cells:
                unique_cells[cell_key] = (x, y, r)
        
        # Compute total score for the section.
        # Score is computed as: score = (total_columns + 1) - col.
        total_columns = len(columns)  # e.g., if there are 6 vertical lines then there are 5 columns.
        section_total_score = 0
        
        # Prepare a mapping of row number to score.
        row_scores = {}
        for (row, col), (x, y, r) in sorted(unique_cells.items(), key=lambda item: (item[0][0], item[0][1])):
            score = (total_columns + 1) - col
            section_total_score += score
            # If a row has multiple cells, you might decide to sum them or choose one.
            # Here we assume one circle per row; if multiple, later ones overwrite.
            row_scores[row] = score
        
        # Print the results in the desired format.
        section_title = section_titles.get(sec_name, sec_name)
        print(f"\n{section_title}:")
        for row_index in sorted(row_scores.keys()):
            question_text = section_questions.get(sec_name, {}).get(row_index, f"Row {row_index}")
            print(f"{row_index}. {question_text}: {row_scores[row_index]}")
        print(f"Total Score: {section_total_score}")
        
        # Store results for the section.
        results[sec_name] = {
            "unique_cells": unique_cells,
            "row_scores": row_scores,
            "total_score": section_total_score,
            "total_columns": total_columns,
            "output": output_c  # Processed section image with circles drawn.
            
        }
        cv2.imshow(sec_name, output_c)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return results

# Example usage:
