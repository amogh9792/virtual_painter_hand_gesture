def fingers_up(lm_list):
    """Detects which fingers are up"""
    tips = [4, 8, 12, 16, 20]
    up = []

    # Thumb
    up.append(1 if lm_list[tips[0]][1] > lm_list[tips[0] - 1][1] else 0)

    # Fingers
    for i in range(1, 5):
        up.append(1 if lm_list[tips[i]][2] < lm_list[tips[i] - 2][2] else 0)

    return up
