import set_env
import language_tool_python

tool: language_tool_python.LanguageTool | None = None


def get_tool():
    global tool
    if not tool:
        tool = language_tool_python.LanguageTool('en-US')
    return tool


def get_errors_in_texts(texts):
    tool = get_tool()

    matches = tool.check(texts)
    return matches


# # Example usage:
# texts = """There are five species of sea turtle species in Taiwan; green turtle, hawksbill, loggerhead, olive ridley, and leatherback. Green sea turtle is the most abundant one. The coast of Taiwan is an important develop site for sea turtles. They utilize the coast as their feeding areas. This study is to describe the diets of green turtles on the east and north coasts of Taiwan, as well as the influence of sites, seasons, gender, and size on the diet selections of green turtles. Turtles were collected from New Taipei City, Keelung City, Yilan County, Miaoli County, and Hualien County. Sixty green turtles with 53 had diet items. The diet composition from the esophagus and stomach of the dead turtles were examined. Results showed that the diets were red algae (86%), green algae (8%), brown algae (6%), artificial debris (0.2%), natural debris (<0.1%), animal (0.1%), and unidentified materials (0.2%). Among the wet weight, red algae was the main diet. A total of 44 macroalgae species were identified, only Pterocladiella capillacea of red algae (IRI: 39) was the most important diet. The major diet changed with different counties and seasons. This may due to the available diet in different places and seasons were different. The diets between males and females were similar. The diet composition in all sizes were similar. Keywords: green turtle, Taiwan, diet, stomach content"""
# #

# number_of_errors = count_errors_in_texts(texts)
# print("Total number of errors found:", number_of_errors)
