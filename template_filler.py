#!/usr/bin/env python

import sys
import re
import json

def main():
  while 1:
    try:
      template = ""
      json_string = ""
      while not json_string:
        json_string = sys.stdin.readline()
        json_string = json_string.strip()

      while not template:
        template = sys.stdin.readline()
        template = template.strip()
    except KeyboardInterrupt:
      break

    if not json_string or not template:
      break

    # json dictionary
    json_dict = json.loads(json_string)

    in_replaceable = False
    replaceable_text = ""
    skip_second_bracket = False

    is_list = False
    skip_list = 0
    end_list = False
    list_key = ""
    save_list_text = False
    write_list = False
    
    is_bool = False
    bool_true = False
    bool_text = ""
    skip_bool = 0
    end_bool = False
    done_bool = False

    len_template = len(template)

    for i in range(0, len_template):

      if skip_second_bracket:
        skip_second_bracket = False
        continue

      if is_list and skip_list > 0:
        skip_list -= 1
        continue

      if save_list_text and skip_list > 0:
        skip_list -= 1
        continue

      if is_bool and skip_bool > 0:
        skip_bool -= 1
        continue

      if end_list and skip_list > 0:
        skip_list -= 1
        if skip_list == 0:
          end_list = False
        continue

      if end_bool and skip_bool > 0:
        skip_bool -= 1
        if skip_bool == 0:
          end_bool = False
        continue

      c = template[i]

      if done_bool and not bool_true:
        if len_template < i + 1 or c != '{' or template[i + 1] != '{':
          continue
        done_bool = False

      if is_bool:
        if template[i + 1] == '}':
          bool_text = bool_text + c
          bool_true = (str(json_dict[bool_text]).lower() == "true")
          is_bool = False
          done_bool = True
          bool_text = ""
        else:
          bool_text = bool_text + c
      elif is_list:
        if template[i + 1] == '}':
          list_key = list_key + c
          is_list = False
          save_list_text = True
          skip_list = 2
        else:
          list_key = list_key + c
      elif save_list_text:
        if len_template > i + 3 and template[i + 3] == '/':
          replaceable_text = replaceable_text + c
          save_list_text = False
          write_list = True
        else:
          replaceable_text = replaceable_text + c
      elif (c != '{' and c != '}') or len_template <= i+1 or (template[i+1] != '{' and template[i+1] != '}'):
        if in_replaceable:
          replaceable_text = replaceable_text + c
        else:
          sys.stdout.write(c)

          if c == ' ':
            sys.stdout.flush()

      else:
        if in_replaceable and len(replaceable_text) > 0:
          # Now replace template
          if '!' != replaceable_text[0]:
            if bool_true:
              sys.stdout.write(replaceable_text)
              bool_true = False
            elif write_list:
              json_obj = json_dict[list_key]
              for obj in json_obj:
                new_string = replaceable_text
                for key, value in obj.items():
                  new_string = re.sub('{{'+re.escape(str(key))+'}}', str(value), new_string)
                sys.stdout.write(new_string)
                sys.stdout.flush()
              write_list = False
            elif '.' in replaceable_text:
              replaceable_text_split = replaceable_text.split('.')
              json_obj = json_dict[replaceable_text_split[0]]
              for k in range(1, len(replaceable_text_split)):
                json_obj = json_obj[replaceable_text_split[k]]

              sys.stdout.write(str(json_obj))
            else:
              sys.stdout.write(str(json_dict[replaceable_text]))
            sys.stdout.flush()
            
          replaceable_text = ""

        if len_template > i+6:
          # each - list
          if template[i+2] == '#' and template[i+3] == 'e':
            is_list = True
            skip_list = 6
        if len_template > i+4:
          # if - bool
          if template[i+2] == '#' and template[i+3] == 'i':
            is_bool = True
            skip_bool = 4
        if len_template > i+3:
          if template[i+2] == "/":
            if template[i+3] == 'i':
              end_bool = True
              skip_bool = 3
            elif template[i+3] == 'e':
              end_list = True
              skip_list = 5
        
        in_replaceable = not in_replaceable
        skip_second_bracket = True

    print("")
    sys.stdout.flush()

        

if __name__ == '__main__':
   main()
