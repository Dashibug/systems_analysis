import json


def interpolate(x, points):
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        if x1 <= x <= x2:
            return y1 + (y2 - y1) * (x - x1) / (x2 - x1)
    return 0


def membership_function(value, fuzzy_set):
    return interpolate(value, fuzzy_set)


def get_membership(value, fuzzy_sets):
    return {term["id"]: membership_function(value, term["points"]) for term in fuzzy_sets}


def apply_rules(temp_degree, heating_degrees, mapping):
    result = 0
    total_weight = 0

    for temp_term, heat_term in mapping:
        temp_value = temp_degree.get(temp_term, 0)
        heat_value = heating_degrees.get(heat_term, 0)

        weight = min(temp_value, heat_value)
        result += weight * heat_value
        total_weight += weight

    return result / total_weight if total_weight > 0 else 0


def task(temp_json, heat_json, rules_json, current_temperature):
    temp_data = json.loads(temp_json)["температура"]
    heat_data = json.loads(heat_json)["температура"]
    rules = json.loads(rules_json)

    temp_degree = get_membership(current_temperature, temp_data)
    heating_degree = get_membership(current_temperature, heat_data)

    result = apply_rules(temp_degree, heating_degree, rules)

    return result


if __name__ == "__main__":
    temp_json = '''{
      "температура": [
          {
          "id": "холодно",
          "points": [
              [0,1],
              [18,1],
              [22,0],
              [50,0]
          ]
          },
          {
          "id": "комфортно",
          "points": [
              [18,0],
              [22,1],
              [24,1],
              [26,0]
          ]
          },
          {
          "id": "жарко",
          "points": [
              [0,0],
              [24,0],
              [26,1],
              [50,1]
          ]
          }
      ]
    }'''

    heat_json = '''{
      "температура": [
          {
            "id": "слабый",
            "points": [
                [0,0],
                [0,1],
                [5,1],
                [8,0]
            ]
          },
          {
            "id": "умеренный",
            "points": [
                [5,0],
                [8,1],
                [13,1],
                [16,0]
            ]
          },
          {
            "id": "интенсивный",
            "points": [
                [13,0],
                [18,1],
                [23,1],
                [26,0]
            ]
          }
      ]
    }'''

    rules_json = '''[
      ["холодно", "интенсивный"],
      ["комфортно", "умеренный"],
      ["жарко", "слабый"]
    ]'''

    current_temperature = 20

    result = task(temp_json, heat_json, rules_json, current_temperature)
    print(f"Значения оптимального управления: {result}")