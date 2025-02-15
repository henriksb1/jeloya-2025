import cv2
import torch
from transformers import YolosForObjectDetection, YolosImageProcessor

print("Loading model...")
model = YolosForObjectDetection.from_pretrained('hustvl/yolos-tiny')
processor = YolosImageProcessor.from_pretrained("hustvl/yolos-tiny")
print("Model ready!")


def detect(image):
    inputs = processor(images=image, return_tensors="pt")
    outputs = model(**inputs)
    target_sizes = torch.tensor([image.shape[:2]])

    # convert outputs (bounding boxes and class logits) to COCO API
    results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.5)[0]

    result_objects = []

    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        box = [round(i, 2) for i in box.tolist()]
        result_objects.append({
            "score": score.item(),
            "label": model.config.id2label[label.item()],
            "box": box,  # [top_left_x, top_left_y, bottom_right_x, bottom_right_y]
        })

    # for result in result_objects:
    #     print(
    #         f"Detected {result['label']} with confidence "
    #         f"{result['score']} at location {result['box']}"
    #     )

    return result_objects


def show_detections(image, results):
    # Show image with bounding boxes
    for result in results:
        score = result['score']
        label = result['label']
        box = result['box']
        box = [round(i, 2) for i in box]
        cv2.rectangle(
            image,
            (int(box[0]), int(box[1])),
            (int(box[2]), int(box[3])),
            (0, 255, 0),
            2,
        )
        cv2.putText(
            image,
            f"{label}: {round(score, 3)}",
            (int(box[0]), int(box[1])),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            2,
        )


def show(image):
    cv2.imshow("Image", cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def grab_webcam():
    print("Starting camera...")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        return
    print("Go!")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame")
                break

            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = detect(frame)
            # print(results)
            try:
                best = max((result for result in results if result['label'] == 'person'),
                           key=lambda result: result['score'])
            except ValueError:
                print("======== You're outside the frame! Move back in! =========")
                continue  # Keep previous reading
            width = frame.shape[1]
            r = best['box'][2]
            l = best['box'][0]
            person_center_x = (r - l) / 2 + l
            direction = person_center_x / width
            print(direction)

            # cv2.imshow('Webcam', cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            # if cv2.waitKey(1) == ord('q'):
            #     break
    finally:
        cap.release()
        cv2.destroyAllWindows()


def main():
    # results = detect(image)
    # show_detections(image, results)
    # show(image)
    grab_webcam()


if __name__ == '__main__':
    main()
