# from django import template
# from django.utils.safestring import mark_safe

# register = template.Library()


# @register.filter
# def parser(content):
#     div_title_added = 0
#     div_section_added = 0
#     lines = content.split('\n')
#     answer = []

#     for line in lines:
#         if (line != ";--------------------------------------------------------"):
#             if (len(line) > 0 and line[0] == ';'):
#                 if (div_section_added > 0):
#                     answer.append(mark_safe("</h6> </div>"))
#                     div_section_added = 0

#                 if (div_title_added == 0):
#                     answer.append(mark_safe("<div class=\"title\"> <b>"))

#                 line1 = line[1:]
#                 answer.append(mark_safe(line1))

#                 div_title_added += 1
#             elif (len(line) > 0):
#                 if (div_title_added > 0):
#                     answer.append(mark_safe("</b></div>"))
#                     div_title_added = 0

#                 if (div_section_added == 0):
#                     answer.append(mark_safe("<div class=\"section\"> <h6>"))

#                 answer.append(mark_safe(line))
#                 div_section_added += 1

#     if (div_title_added > 0):
#         answer.append(mark_safe("</b></div>"))
#     elif (div_section_added > 0):
#         answer.append(mark_safe(" </h6> </div>"))

#     safe_answer = mark_safe(answer)

#     return safe_answer