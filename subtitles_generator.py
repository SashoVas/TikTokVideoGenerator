from PIL import Image, ImageDraw, ImageFont


class SubtitlesGenerator:
    def __init__(self, font_size=60, max_width=1000, padding=10) -> None:
        self.font_size = font_size
        self.max_width = max_width
        self.padding = padding

    def create_image_with_text_transparent(self, text, output_path='images/output_image.png'):
        # Initialize ImageDraw to determine text size
        font = ImageFont.truetype("arial.ttf", self.font_size)
        # Transparent dummy image
        dummy_image = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
        draw = ImageDraw.Draw(dummy_image)

        # Text wrapping function
        def wrap_text(text, font, max_width):
            lines = []
            words = text.split(' ')
            while words:
                line = ''
                while words and draw.textbbox((0, 0), line + words[0], font=font)[2] <= max_width:
                    line += (words.pop(0) + ' ')
                lines.append(line)
            return lines

        # Wrap text to fit within the specified maximum width
        wrapped_text = wrap_text(text, font, self.max_width)

        # Calculate image dimensions based on wrapped text
        max_line_width = max(draw.textbbox((0, 0), line, font=font)[
                             2] for line in wrapped_text)
        total_text_height = sum(draw.textbbox((0, 0), line, font=font)[
                                3] for line in wrapped_text)

        # Add padding to the image dimensions
        width = max_line_width + 2 * self.padding
        height = total_text_height + 2 * self.padding + len(wrapped_text) * 5

        # Create a new image with transparent background
        image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        # Draw the wrapped text on the image with shadow for better visibility
        y_position = self.padding
        for line in wrapped_text:
            # Shadow
            draw.text((self.padding + 2, y_position + 2), line,
                      fill='gray', font=font)  # Shadow in gray
            # Main text
            draw.text((self.padding, y_position), line,
                      fill='black', font=font)  # Main black text
            # Add padding between lines
            y_position += draw.textbbox((0, 0), line, font=font)[3] + 5

        # Save the image with transparent background
        image.save(output_path, "PNG")
        print(f"Image saved to {output_path}")

    def create_image_with_text(self, text, output_path='images/output_image.png'):
        # Initialize ImageDraw to determine text size
        # You may need to adjust the font path
        font = ImageFont.truetype("arial.ttf", self.font_size)
        # Create a dummy image to get text size
        dummy_image = Image.new('RGB', (1, 1))
        draw = ImageDraw.Draw(dummy_image)

        # Define text wrapping function
        def wrap_text(text, font, max_width):
            lines = []
            words = text.split(' ')
            while words:
                line = ''
                while words and draw.textbbox((0, 0), line + words[0], font=font)[2] - draw.textbbox((0, 0), line + words[0], font=font)[0] <= max_width:
                    line += (words.pop(0) + ' ')
                lines.append(line)
            return lines

        # Wrap text to fit within the specified maximum width
        wrapped_text = wrap_text(text, font, self.max_width)

        # Calculate image dimensions based on wrapped text
        max_line_width = max(draw.textbbox((0, 0), line, font=font)[
            2] - draw.textbbox((0, 0), line, font=font)[0] for line in wrapped_text)
        total_text_height = sum(draw.textbbox((0, 0), line, font=font)[
                                3] - draw.textbbox((0, 0), line, font=font)[1] for line in wrapped_text)

        # Add padding to the image dimensions
        width = max_line_width + 2 * self.padding
        height = total_text_height + 2 * self.padding + len(wrapped_text)*5

        # Create a new image with calculated dimensions
        image = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(image)

        # Draw the wrapped text on the image
        y_position = self.padding
        for line in wrapped_text:
            draw.text((self.padding, y_position),
                      line, fill='black', font=font)
            y_position += draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox(
                (0, 0), line, font=font)[1] + 5  # Adding some padding between lines

        # Save the image
        image.save(output_path)
        print(f"Image saved to {output_path}")
