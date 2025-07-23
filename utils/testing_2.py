import os
import shutil
import sys
from time import sleep

def clear_screen() -> None:
    os.system('clear||cls')

# Define your multi-line strings exactly as they are now, with the .replace()
# IMPORTANT: Ensure NO blank line immediately after the opening """ for GAMEOVER_ART and WINNER_ART.
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
"""

WINNER_ART ="""   * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
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

other_strings = {
    "gameover": GAMEOVER_ART,
    "winner_mark": WINNER_ART,
}

winner_mark = "winner_mark"

def center_multiline_string(multiline_str: str, terminal_width: int) -> str:
    lines = multiline_str.strip().split('\n')

    max_line_width = 0
    for line in lines:
        if line.strip():
            max_line_width = max(max_line_width, len(line))
    
    if max_line_width == 0: return ""

    centered_lines = []
    for line in lines:
        padded_line = line.ljust(max_line_width)
        centered_lines.append(padded_line.center(terminal_width))
        
    return "\n".join(centered_lines)


print("\n--- Diagnostic AFTER .replace() ---")

# Access the processed strings from the dictionary for diagnostic
processed_gameover = other_strings["gameover"]
processed_winner = other_strings["winner_mark"]

go_lines_processed = processed_gameover.strip().split('\n')
win_lines_processed = processed_winner.strip().split('\n')

print("\nGAMEOVER_ART First Line (after .replace()):")
print(f"Length: {len(go_lines_processed[0])}")
print(f"Repr: {repr(go_lines_processed[0])}")
if '\xa0' in go_lines_processed[0]:
    print("!!! WARNING: \\xa0 still present in GAMEOVER_ART first line after replace !!!")

print("\nWINNER_ART First Line (after .replace()):")
print(f"Length: {len(win_lines_processed[0])}")
print(f"Repr: {repr(win_lines_processed[0])}")
if '\xa0' in win_lines_processed[0]:
    print("!!! WARNING: \\xa0 still present in WINNER_ART first line after replace !!!")

print("\n--- Diagnostic END ---")
sleep(2)

print("Starting multi-line centering test...")
sleep(5)

for i in range(5):
    columns = shutil.get_terminal_size().columns

    if i % 2 == 0:
        string_to_print = processed_gameover # Use the pre-processed string
    else:
        string_to_print = processed_winner   # Use the pre-processed string

    centered_output = center_multiline_string(string_to_print, columns)

    clear_screen()
    print(centered_output)
    sys.stdout.flush()

    sleep(0.75)

clear_screen()
print("Multi-line centering test finished.")
print(f"Your terminal reported a width of: {shutil.get_terminal_size().columns} columns.")
print("If the issue persists, please share the *exact* output of the 'Diagnostic AFTER .replace()' section.")
# import shutil

# # IMPORTANT: Ensure NO blank line immediately after the opening """ for GAMEOVER_ART.
# # The first character of your art should be right after the triple quotes.
# GAMEOVER_ART = """
#    * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#    *                                                                         *
#    *                                                                         *
#    *               * * *        **        *       *    * * * *               *
#    *              *            *  *       * *   * *    *                     *
#    *              *   * *     *    *      *   *   *    * * *                 *
#    *              *     *    *      *     *       *    *                     *
#    *               * * *    *        *    *       *    * * * *               *
#    *                                                                         *
#    *                                                                         *
#    *                *  *     *       *    * * * *     *  *  *                *
#    *              *      *    *     *     *           *      *               *
#    *              *      *     *   *      * * *       *  *  *                *
#    *              *      *      * *       *           *      *               *
#    *                *  *         *        * * * *     *       *              *
#    *                                                                         *
#    *                                                                         *
#    * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
# """

# def center_multiline_string_diagnostic(multiline_str: str, terminal_width: int):
#     lines = multiline_str.strip().split('\n')

#     max_line_width = 0
#     for line in lines:
#         if line.strip():
#             max_line_width = max(max_line_width, len(line))
    
#     if max_line_width == 0: return ""

#     print(f"\n--- Diagnostic for `center_multiline_string` ---")
#     print(f"Terminal width reported: {terminal_width}")
#     print(f"Calculated max_line_width of art: {max_line_width}")
    
#     first_line_original = lines[0]
#     first_line_padded = first_line_original.ljust(max_line_width)
#     first_line_centered = first_line_padded.center(terminal_width)

#     print(f"\nOriginal first line (len {len(first_line_original)}): {repr(first_line_original)}")
#     print(f"Padded first line (len {len(first_line_padded)}): {repr(first_line_padded)}")
#     print(f"Centered first line (len {len(first_line_centered)}): {repr(first_line_centered)}")
    
#     print("\n--- Visual Check (copy-paste this exactly into a text editor) ---")
#     print(first_line_centered)
#     print("-----------------------------------------------------------------") # 65 hyphens for reference

#     # Also show a later line's processing for comparison
#     if len(lines) > 1:
#         second_line_original = lines[1]
#         second_line_padded = second_line_original.ljust(max_line_width)
#         second_line_centered = second_line_padded.center(terminal_width)
#         print(f"\nOriginal second line (len {len(second_line_original)}): {repr(second_line_original)}")
#         print(f"Padded second line (len {len(second_line_padded)}): {repr(second_line_padded)}")
#         print(f"Centered second line (len {len(second_line_centered)}): {repr(second_line_centered)}")
#         print("\n--- Visual Check (Second Line) ---")
#         print(second_line_centered)
#         print("-----------------------------------------------------------------")


# # Run the diagnostic
# terminal_columns = shutil.get_terminal_size().columns
# center_multiline_string_diagnostic(GAMEOVER_ART, terminal_columns)