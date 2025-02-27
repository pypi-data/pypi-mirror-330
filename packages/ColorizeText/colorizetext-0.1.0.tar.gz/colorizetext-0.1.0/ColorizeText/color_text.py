class ColorText:

    @classmethod
    def color(cls, text, color):
        color_code = cls.COLORS.get(color.lower(), cls.COLORS["reset"])
        return f"{color_code}{text}{cls.COLORS['reset']}"

    @classmethod
    def bold(cls, text):
        return cls.color(text, "bold")
        
    @classmethod
    def underline(cls, text):
        return cls.color(text, "underline")

    @classmethod
    def rainbow(cls, text):
        colors = ["red", "yellow", "green", "cyan", "blue", "magenta"]
        result = ""
        for i, char in enumerate(text):
            result += cls.color(char, colors[i % len(colors)])
        return result
    
