import global_vars
import webbrowser
import os
#####################################################
# Ref Treant.js https://fperucic.github.io/treant-js/ 
# 
#
#####################################################
class VisualSitemap(object):
	def __init__(self):
		# default values for beginning/ending of HTML file
		self.prefix_html = "<html><head><title>Website Visual Sitemap</title>\n" \
						   "<link rel=\"stylesheet\" href=\"js/Treant.css\">\n" \
						   "<link rel=\"stylesheet\" href=\"js/connectors.css\">\n" \
						   "<script src=\"js/raphael.js\"></script>\n" \
						   "<script src=\"js/Treant.js\"></script>\n</head>\n<body>\n<div id=\"treemap-chart\"></div>\n<script>\n"

		self.suffix_html = "</script>\n</body>\n</html>"
		self.js_string = ""

	# build the JS string that runs the tree structure
	def build(self):
		js_prefix = "    var chart_config = {\n" \
							"        chart: {\n" \
							"            container: \"#treemap-chart\",\n" \
							"            levelSeparation: 25,\n" \
							"            connectors: {" \
							"                type: \"step\",\n" \
							"                style: {" \
							"                    \"stroke-width\": 1\n" \
							"                }\n" \
							"            },\n" \
							"            node: {\n" \
							"                HTMLclass: \"treemap\"," \
							"				 collapsable: true," \
							"            }\n" \
							"       },\n" \
							"       nodeStructure: {" \
							"           text: { name: \"" + global_vars.starting_url + "\" },\n" \
							"           connectors: {" \
							"               style: {\n" \
							"                   'stroke': '#bbb',\n" \
							"                   'arrow-end': 'block-wide-long'\n" \
							"               }\n" \
							"           },\n" \
							"       children: [\n"
		js_nodes = ""
		parent_url_count = 1
		parent_url_length = len(global_vars.url_tree)
		for parent_url in sorted(global_vars.url_tree):
			if parent_url == "/":
				continue
			

			if parent_url_count == parent_url_length:
				# DEF META mit Links
				js_nodes += "        {\n" \
									"			text: {\n" \
									"				name: \" MetaLinkPhase\",\n" \
									"				title: \"One of kind\",\n" \
									"				desc: \"A basic example\",\n" \
									"				contact: { \n" \
									"					val: \"contact me\",\n" \
									"					href: \"http://twitter.com/\",\n" \
									"					target: \"_self\"\n" \
									"				}\n" \
									"}"                    

				if len(global_vars.url_tree[parent_url]) > 0:
					child_url_length = len(global_vars.url_tree[parent_url])
					if child_url_length > global_vars.child_nodes:
						child_url_length = global_vars.child_nodes
					child_url_count = 1
					js_nodes += ",\n           children: [\n"
					for child_url in global_vars.url_tree[parent_url]:
						if child_url_count == child_url_length:
							if child_url_length < global_vars.child_nodes:
								js_nodes += "           { \n" \
										"text: { name: \"META-A" + child_url + "\" } }"
							else:
								js_nodes += "           { \n" \
										"text: { name: \"META-B" + child_url + "\" } },"
								js_nodes += "           { \n" \
										"text: { name: \"..." + str(len(global_vars.url_tree[parent_url]) - child_url_length) + " more pages \" } }"
							break
						else:
							js_nodes += "{ " \
									"text: { name: \"META-GO" + child_url + "\" } },"
							child_url_count += 1

					js_nodes += "]\n"
				js_nodes += "}\n"
			else:
				#parent_url_clean = parent_url.replace('//', '')
				js_nodes += "       {\n" \
									"           text: { \n" \
									"					name: \"META-TOP" + parent_url + "\", \n" \
									"					contact: { \n" \
									"						val: \""+ parent_url + "\",\n" \
									"						href: \""+ parent_url + "\",\n" \
									"						target: \"_blank\"\n" \
									"					}\n" \
									"			},\n" \
									"           stackChildren: true,\n" \
									"           connectors: {\n" \
									"               style: {\n" \
									"                   'arrow-end': 'block-wide-long'\n" \
									"               }\n" \
									"           }" 
									
									
				# need to plan children
				
				if len(global_vars.url_tree[parent_url]) > 0:
					child_url_length = len(global_vars.url_tree[parent_url])
					if child_url_length > global_vars.child_nodes:
						child_url_length = global_vars.child_nodes
					child_url_count = 1
					
					
					js_nodes += ",\n           children: [ \n"
					for child_url in sorted(global_vars.url_tree[parent_url]):
						child_url = child_url.replace('https:/', '') 
						child_url = parent_url + child_url
						# TEST Above
						
						if child_url_count == child_url_length:
							if child_url_length < global_vars.child_nodes:
								
								js_nodes += "           { \n" \
										"text: {\n" \
												 "name: \"META-PLAN1" + child_url + "\", \n" \
												 "contact: {\n" \
												 "		val:  \""+ child_url + "\",\n" \
												 "		href: \""+ child_url + "\",\n" \
												 "		target: \"_blank\"\n" \
												 " }\n" \
												 "} }"
							else:
								js_nodes += "           { \n" \
										"text: { \n" \
												"name: \"META-PLAN2" + child_url + "\", \n" \
												"contact: { \n" \
														"val: \""+ child_url + "\",\n" \
														"href: \""+ child_url + "\",\n" \
														"target: \"_blank\"\n" \
												"}\n" \
												"} },"
								js_nodes += "           { \n" \
										"text: { name: \"..." + str(len(global_vars.url_tree[parent_url]) - child_url_length) + " more pages \" } }"
							break
						else:
							js_nodes += "{ " \
											"text: { \n" \
													"name: \"META-LAST" + child_url + "\", \n" \
												    "contact: {\n" \
												    	"val:  \""+ child_url + "\",\n" \
												    	"href: \""+ child_url + "\",\n" \
												    	"target: \"_blank\"\n" \
												    " }\n" \
												   "} \n" \
										"},"
							child_url_count += 1

					js_nodes += "]\n"
				
				js_nodes += "},\n"
				
				parent_url_count += 1

		js_suffix = "] }\n};\nnew Treant( chart_config );\n" 
		self.js_string = js_prefix + js_nodes + js_suffix
		self.save()

	# builds HTML file for viewing the tree structure and displays the webpage in default browser
	def save(self):
		with open("index.html", "w") as f:
			f.writelines(self.prefix_html)
			f.writelines(self.js_string)
			f.writelines(self.suffix_html)
			#webbrowser.open('file://' + os.path.realpath("index.html"))