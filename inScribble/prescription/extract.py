def extract_info(data):
    new_data = []
    for unit in data["recognitionUnits"]:
        if unit["class"] == "leaf":
            if unit["category"] == "inkWord":
                text = unit["recognizedText"]
                bounding_rectangle = unit["boundingRectangle"]
                new_data.append({"text": text, "area": bounding_rectangle})
            elif unit["category"] in ["inkBullet", "inkDrawing"]:
                bounding_rectangle = unit["boundingRectangle"]
                text = "HOLLLOOOO"
                new_data.append({"text": text, "area": bounding_rectangle})

    new_data.sort(key=lambda x: x["area"]["topY"])

    count = 0
    name = ""
    final_data = []
    for doc in new_data:
        if doc["text"] == "HOLLLOOOO":
            count += 1
        else:
            if name:
                final_data.append({"name": name, "count": count})
            name = doc["text"]
            count = 0

    if (final_data and final_data[-1]["name"] != name) or count or name:
        final_data.append({"name": name, "count": count})

    # return new_data
    return final_data
