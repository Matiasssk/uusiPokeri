# detect_cards.py
import cv2
import os
import numpy as np

# Polut templateihin ja screenshottiin
TEMPLATE_DIR = "./poker_card_detection_template/cards"
SCREENSHOT_PATH = "./poker_card_detection_template/screenshots/example_table.png"

# Lataa kaikki template-kuvat muotoon {"As": kuva, "Kd": kuva, ...}
def load_templates():
    templates = {}
    for fname in os.listdir(TEMPLATE_DIR):
        if fname.endswith(".png"):
            card_code = os.path.splitext(fname)[0]
            path = os.path.join(TEMPLATE_DIR, fname)
            templates[card_code] = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    return templates

def find_cards(image, templates, threshold=0.85):
    detected = []
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    for card, tmpl in templates.items():
        res = cv2.matchTemplate(img_gray, tmpl, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            detected.append((card, pt, res[pt[1], pt[0]]))
    return detected

if __name__ == "__main__":
    image = cv2.imread(SCREENSHOT_PATH)
    templates = load_templates()
    detected_cards = find_cards(image, templates)

    # Poistetaan päällekkäiset ja valitaan vahvimmat osumat
    unique = {}
    for card, pt, score in detected_cards:
        if card not in unique or score > unique[card][1]:
            unique[card] = (pt, score)

    print("Tunnistetut kortit (vahvuus):")
    for card, (pt, score) in unique.items():
        print(f"{card} at {pt} (score: {score:.2f})")

    # Piirrä tunnistukset
    for card, (pt, _) in unique.items():
        tmpl = templates[card]
        h, w = tmpl.shape
        cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)
        cv2.putText(image, card, (pt[0], pt[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.imwrite("detected_output.png", image)
    print("Tallennettu kuva: detected_output.png")
