{
        chart: {
            container: "#treemap-chart",
            levelSeparation: 25,
            connectors: {                type: "step",
                style: {                    "stroke-width": 1
                }
            },
            node: {
                HTMLclass: "treemap",				 collapsable: true,            }
       },
       nodeStructure: {           text: { name: "https://orf.at" },
           connectors: {               style: {
                   'stroke': '#bbb',
                   'arrow-end': 'block-wide-long'
               }
           },
       children: [
       {
           text: { 
					name: "//", 
					contact: { 
						val: "//",
						href: "//",
						target: "_blank"
					}
			},
           stackChildren: true,
           connectors: {
               style: {
                   'arrow-end': 'block-wide-long'
               }
           },
           children: [ 
{
           text: { 
					name: "https:/orf.at/", 
					contact: { 
						val: "https:/orf.at/",
						href: "https:/orf.at/",
						target: "_blank"
					}
			},
           stackChildren: true,
           connectors: {
               style: {
                   'arrow-end': 'block-wide-long'
               }
           },           { 
text: { name: "META-PLAN1https:/orf.at/" } }]
},
       {
           text: { 
					name: "//orf.at/", 
					contact: { 
						val: "//orf.at/",
						href: "//orf.at/",
						target: "_blank"
					}
			},
           stackChildren: true,
           connectors: {
               style: {
                   'arrow-end': 'block-wide-long'
               }
           },
           children: [ 
{
           text: { 
					name: "https:/push/", 
					contact: { 
						val: "https:/push/",
						href: "https:/push/",
						target: "_blank"
					}
			},
           stackChildren: true,
           connectors: {
               style: {
                   'arrow-end': 'block-wide-long'
               }
           },           { 
text: { name: "META-PLAN1https:/uebersicht/" } }]
},
        {
			text: {
				name: " MetaLinkPhase",
				title: "One of kind",
				desc: "A basic example",
				contact: { 
					val: "contact me",
					href: "http://twitter.com/",
					target: "_self"
				}
},
           children: [
{ text: { name: "META-GOhttps:/3344859/" } },{ text: { name: "META-GOhttps:/3344818/" } },{ text: { name: "META-GOhttps:/3344821/" } },{ text: { name: "META-GOhttps:/3344877/" } },           { 
text: { name: "META-Bhttps:/impressum-nachrichtenagenturen/" } },           { 
text: { name: "...38 more pages " } }]
}
] }
}