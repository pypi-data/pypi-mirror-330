
def print_separator(text=""):
    def gradient_color_bg(start_rgb, mid_rgb, end_rgb, steps):
        """
        Generates a smooth gradient_colors background transitioning through three colors.
        
        todo: assign colors, number of lines
        """
        r1, g1, b1 = start_rgb
        r2, g2, b2 = mid_rgb
        r3, g3, b3 = end_rgb

        gradient_colors = []

        # First transition: Dark Green → Dark Cyan
        for i in range(steps // 2):
            t = i / ((steps // 2) - 1)
            r = int(r1 + (r2 - r1) * t)
            g = int(g1 + (g2 - g1) * t)
            b = int(b1 + (b2 - b1) * t)
            gradient_colors.append(f"\033[48;2;{r};{g};{b}m ")  # Background color

        # Second transition: Dark Cyan → Dark Blue
        for i in range(steps // 2, steps):
            t = (i - (steps // 2)) / ((steps // 2) - 1)
            r = int(r2 + (r3 - r2) * t)
            g = int(g2 + (g3 - g2) * t)
            b = int(b2 + (b3 - b2) * t)
            gradient_colors.append(f"\033[48;2;{r};{g};{b}m ")  # Background color

        return gradient_colors

    reset = "\033[0m"
    text_color = "\033[1;37m"  # White text
    width = 120  # Fixed width

    # Darker Loguru colors
    dark_green = (0, 125, 5)  # #007D05
    dark_cyan = (0, 139, 141)  # #008B8D
    dark_blue = (58, 64, 156)  # #3A409C

    third_width = width // 2  # Each gradient_colors step is half width (mirrored)
    gradient_half1 = gradient_color_bg(dark_green, dark_cyan, dark_blue, third_width)
    gradient_half2 = gradient_color_bg(dark_blue, dark_cyan, dark_green, third_width)
    gradient = gradient_half1 + gradient_half2  # Mirror the gradient_colors


    # Print the gradient_colors with centered text
    print("".join(gradient) + reset)
    
    if text:
        text_start = (width - len(text)) // 2
        print(
            "".join(gradient[:text_start])
            + text_color
            + text
            + reset
            + "".join(gradient[text_start + len(text):])
            + reset
        )
        print("".join(gradient) + reset)
