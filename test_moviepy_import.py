# Test import for moviepy.editor
try:
    from moviepy.editor import ImageSequenceClip
    print("moviepy.editor import successful!")
except ImportError as e:
    print(f"ImportError: {e}")
