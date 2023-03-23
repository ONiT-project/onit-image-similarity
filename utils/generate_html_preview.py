import json

with open('../data/neighbours/neighbours.json') as file:
  data = json.load(file)

  sections = []

  for neighbourhood in data:
    ref = neighbourhood['reference']

    html_list = ''

    for n in neighbourhood['neighbours']:
      html_list += f'''<li><img src="{n['iiif_url']}" title="{n['id'] + ' Score: ' + str(n['score'])}"></li>\n'''

    sections.append(f'''
      <section>
        <div class="ref">
          <img src="{ref['iiif_url']}" title="{ref['id']}"/>
        </div>
        <ul>
          {html_list}
        </ul>
      </section>''')
  
  markup = f'''
    <!DOCTYPE html>
    <html>
      <head>
        <title>ONiT | Image Similarity</title>
        <style>
          html, body {{
            padding: 0;
            margin: 0;
          }}

          img {{
            max-width: 200px;
            max-height: 200px;
          }}

          .ref {{
            padding: 10px;
            width: 100%;
            background-color: #efefef;
          }}

          ul {{
            list-style-type: none;
          }}

          li {{
            display: inline-block;
            margin: 10px 10px 0 0;
          }}
        </style>
      </head>

      <body>
        {''.join(sections)}
      </body>
    </html>
    '''
  
  with open('../data/neighbours/index.html', 'w') as outfile:
    outfile.write(markup)
    outfile.close()

