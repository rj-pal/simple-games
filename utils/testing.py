import os
import shutil
import sys
from time import sleep

# Your provided clear_screen function
def clear_screen() -> None:
    """Clears the terminal screen."""
    os.system('clear||cls') # This is a good cross-platform attempt

# ---- Game Outcome Banners ----
# A large ASCII art banner displayed when any game concludes or a player wins.
GAMEOVER = """
   * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
   *                                                                         *
   *                                                                         *
   *               * * *        **        *       *    * * * *               *
   *              *            *  *       * *   * *    *                     *
   *              *   * *     *    *      *   *   *    * * *                 * 
   *              *     *    *      *     *       *    *                     *
   *               * * *    *        *    *       *    * * * *               *
   *                                                                         *
   *                                                                         *
   *                *  *     *       *    * * * *     *  *  *                *
   *              *      *    *     *     *           *      *               *
   *              *      *     *   *      * * *       *  *  *                *
   *              *      *      * *       *           *      *               *
   *                *  *         *        * * * *     *       *              *
   *                                                                         *
   *                                                                         *
   * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
"""
# A large ASCII art banner displayed when the player 'X' wins in Tic Tac Toe.
XWINS = """
   * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
   *                                                                         *
   *                                                                         *
   *                            *       *                                    *
   *                              *   *                                      *
   *                                *                                        *
   *                              *   *                                      *
   *                            *       *                                    *
   *                                                                         *
   *         *             *     * * *      *       *       * * *            *
   *         *             *       *        *  *    *      *     *           *
   *          *     *     *        *        *    *  *        *               *
   *           *  *   *  *         *        *       *      *    *            *
   *            *       *        * * *      *       *       * * *            *
   *                                                                         *
   *                                                                         *
   * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
"""
# A large ASCII art banner displayed when the player 'O' wins in Tic Tac Toe.
OWINS = """
   * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
   *                                                                         *
   *                                                                         *
   *                            *   *                                        *
   *                          *       *                                      *
   *                          *       *                                      *
   *                          *       *                                      *
   *                            *   *                                        *
   *                                                                         *
   *         *             *     * * *      *       *       * * *            *
   *         *             *       *        *  *    *      *     *           *
   *          *     *     *        *        *    *  *        *               *
   *           *  *   *  *         *        *       *      *    *            *
   *            *       *        * * *      *       *       * * *            *
   *                                                                         *
   *                                                                         *
   * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
"""

# Example strings
other_strings = {
    "gameover": GAMEOVER,
    "winner_mark": XWINS,
}

winner_mark = "winner_mark"

import os
import shutil
import sys
from time import sleep

# Your provided clear_screen function
def clear_screen() -> None:
    """Clears the terminal screen."""
    os.system('clear||cls')

# Define your multi-line strings
GAMEOVER_ART = """
   * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
   * *
   * *
   * * * * ** * * * * * * *
   * * * * * * * * * *
   * * * * * * * * * * * * *
   * * * * * * * * *
   * * * * * * * * * * * * *
   * *
   * *
   * * * * * * * * * * * * *
   * * * * * * * * *
   * * * * * * * * * * * *
   * * * * * * * * *
   * * * * * * * * * * *
   * *
   * *
   * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
"""
GAMEOVER_ART = """
   * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
   *                                                                         *
   *                                                                         *
   *               * * *        **        *       *    * * * *               *
   *              *            *  *       * *   * *    *                     *
   *              *   * *     *    *      *   *   *    * * *                 *
   *              *     *    *      *     *       *    *                     *
   *               * * *    *        *    *       *    * * * *               *
   *                                                                         *
   *                                                                         *
   *                *  *     *       *    * * * *     *  *  *                *
   *              *      *    *     *     *           *      *               *
   *              *      *     *   *      * * *       *  *  *                *
   *              *      *      * *       *           *      *               *
   *                *  *         *        * * * *     *       *              *
   *                                                                         *
   *                                                                         *
   * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
""".replace('\xa0', ' ')

# Let's create a placeholder for WINNER_ART for the example
WINNER_ART = """
 _______ _    _ _____  _   _  _____   _______ _______ _    _
|__   __| |  | |  __ \| \ | |/ ____| |__   __|__   __| |  | |
   | |  | |__| | |__) |  \| | |  __     | |     | |  | |__| |
   | |  |  __  |  _  /| . ` | | |_ |    | |     | |  |  __  |
   | |  | |  | | | \ \| |\  | |__| |    | |     | |  | |  | |
   |_|  |_|  |_|_|  \_\_| \_|\_____|    |_|     |_|  |_|  |_|

"""
WINNER_ART =""" * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
   *                                                                         *
   *                                                                         *
   *                            *       *                                    *
   *                              *   *                                      *
   *                                *                                        *
   *                              *   *                                      *
   *                            *       *                                    *
   *                                                                         *
   *         *             *     * * *      *       *       * * *            *
   *         *             *       *        *  *    *      *     *           *
   *          *     *     *        *        *    *  *        *               *
   *           *  *   *  *         *        *       *      *    *            *
   *            *       *        * * *      *       *       * * *            *
   *                                                                         *
   *                                                                         *
   * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
"""

# Store them in your dictionary (or directly use the variables)
other_strings = {
    "gameover": GAMEOVER_ART,
    "winner_mark": WINNER_ART,
}

winner_mark = "winner_mark"

def center_multiline_string(multiline_str: str, terminal_width: int) -> str:
    lines = multiline_str.strip().split('\n') # .strip() removes leading/trailing blank lines

    centered_lines = []
    for i, line in enumerate(lines):
        # We're relying on the assertion that all lines are already the same length (85).
        # So, no max_line_width or ljust is needed.
        
        # If the first line is consistently off by one to the left, we can try this adjustment.
        # This is a bit of a hack, but sometimes necessary for visual perfection.
        # UNCOMMENT THE FOLLOWING BLOCK ONLY IF DIAGNOSTICS DON'T REVEAL HIDDEN CHARS/LENGTH ISSUES
        # if i == 0 and line.strip(): # Check if it's the first non-empty line
        #     # Try adding one extra space to the left padding for the first line
        #     # This means manually calculating padding instead of relying purely on .center()
        #     current_len = len(line)
        #     total_padding = terminal_width - current_len
        #     if total_padding > 0:
        #         left_pad = (total_padding // 2) + 1 # Add one extra space to left
        #         right_pad = total_padding - left_pad
        #         centered_line = " " * left_pad + line + " " * right_pad
        #     else:
        #         centered_line = line # Or truncate if too long
        # else:
        #     centered_line = line.center(terminal_width)
        # centered_lines.append(centered_line)
        
        # Original simpler approach if all lines are same length:
        centered_lines.append(line.center(terminal_width))
        
    return "\n".join(centered_lines)
def center_multiline_string(multiline_str: str, terminal_width: int) -> str:
    lines = multiline_str.strip().split('\n')

    # Since all your lines are now 78, max_line_width will be 78.
    # We still keep this calculation for robustness, in case you change your art later.
    max_line_width = 0
    for line in lines:
        if line.strip():
            max_line_width = max(max_line_width, len(line))
    
    if max_line_width == 0: return ""

    centered_lines = []
    for line_index, line in enumerate(lines): # Use enumerate to get line_index
        # No need for padded_line = line.ljust(max_line_width) if all lines are already max_line_width
        # But if they are, ljust does nothing, so it's harmless to keep.
        # Let's keep it for future proofing if art line lengths vary again.
        padded_line = line.ljust(max_line_width) # Ensures all art lines are 78 chars long

        # --- Manual Offset Hack for Visual Perfection ---
        # This targets the first line (index 0)
        # You might need to adjust the '+1' to '+2' if it's still off by more.
        if line_index == 0: # Only apply this special handling to the first line
            current_art_width = len(padded_line) # This should be 78
            total_padding_needed = terminal_width - current_art_width

            if total_padding_needed > 0:
                # Calculate the left padding as normal, then add 1 more space
                left_padding = (total_padding_needed // 2) + 4 # Add an extra space to the left
                right_padding = total_padding_needed - left_padding
                centered_lines.append(" " * left_padding + padded_line + " " * right_padding)
            else:
                centered_lines.append(padded_line) # Fallback if terminal is too narrow
        else:
            # For all other lines, use the standard centering (which should now work perfectly)
            centered_lines.append(padded_line.center(terminal_width))
        # --- End Manual Offset Hack ---
        
    return "\n".join(centered_lines)


print("\n--- DIAGNOSTIC START ---")

print("\n--- GAMEOVER_ART Diagnostics ---")
go_lines = GAMEOVER_ART.strip().split('\n')
print(f"GAMEOVER_ART first line (repr): {repr(go_lines[0])}")
for i, line in enumerate(go_lines):
    print(f"GAMEOVER_ART line {i}: Length = {len(line)}")
    if len(line) != 85:
        print(f"  *** WARNING: This line's length is NOT 85! ***")

print("\n--- WINNER_ART Diagnostics ---")
win_lines = WINNER_ART.strip().split('\n')
print(f"WINNER_ART first line (repr): {repr(win_lines[0])}")
for i, line in enumerate(win_lines):
    print(f"WINNER_ART line {i}: Length = {len(line)}")
    if len(line) != 85:
        print(f"  *** WARNING: This line's length is NOT 85! ***")

print("\n--- DIAGNOSTIC END ---\n")
sleep(5) # Give time to read diagnostics before animation starts

print("Starting multi-line centering test (without max_line_width padding)...")
sleep(1)

for i in range(5):
    columns = shutil.get_terminal_size().columns

    if i % 2 == 0:
        string_to_print = other_strings["gameover"]
    else:
        string_to_print = other_strings[winner_mark]

    centered_output = center_multiline_string(string_to_print, columns)

    clear_screen()
    print(centered_output)
    sys.stdout.flush()

    sleep(0.75)

clear_screen()
print("Multi-line centering test finished.")
print(f"Your terminal reported a width of: {shutil.get_terminal_size().columns} columns.")
print("If the first line is still off, check the diagnostic output carefully.")

def center_multiline_string(multiline_str: str, terminal_width: int) -> str:
    """
    Centers a multi-line string (like ASCII art) within the terminal width.
    Each line of the art is centered relative to the widest line in the art,
    and then the entire block is centered.
    """
    lines = multiline_str.strip().split('\n')

    # 1. Find the maximum width of any line in the ASCII art
    max_line_width = 0
    for line in lines:
        if line.strip(): # Only consider non-empty lines for max_line_width calculation
            max_line_width = max(max_line_width, len(line))
    
    if max_line_width == 0:
        return "" # Return empty if no content

    centered_lines = []
    for line in lines:
        # 2. Pad each line to the max_line_width of the art.
        # This preserves the internal structure and makes the entire art block uniform.
        padded_line = line.ljust(max_line_width)
        
        # 3. Now, center this uniformly-padded line within the terminal width.
        centered_lines.append(padded_line.center(terminal_width))
        
    return "\n".join(centered_lines)


print("Starting multi-line centering test (with proper max_line_width handling)...")
sleep(1)

for i in range(5):
    columns = shutil.get_terminal_size().columns

    if i % 2 == 0:
        string_to_print = other_strings["gameover"]
    else:
        string_to_print = other_strings[winner_mark]

    centered_output = center_multiline_string(string_to_print, columns)

    clear_screen()
    print(centered_output)
    sys.stdout.flush()

    sleep(0.75)

clear_screen()
print("Multi-line centering test finished.")
print(f"Your terminal reported a width of: {shutil.get_terminal_size().columns} columns.")
print("The ASCII art should now be perfectly centered and visually coherent.")
