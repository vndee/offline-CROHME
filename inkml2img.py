import numpy as np
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET

def get_label(inkml_file_abs_path):
    tree = ET.parse(inkml_file_abs_path)
    root = tree.getroot()
    doc_namespace = "{http://www.w3.org/2003/InkML}"

    for child in root:
        if child.tag == doc_namespace + 'annotation' and child.attrib == {'type': 'truth'}:
            return child.text.strip()
    return ""

def get_traces_data(inkml_file_abs_path):
    traces_data = []

    tree = ET.parse(inkml_file_abs_path)
    root = tree.getroot()
    doc_namespace = "{http://www.w3.org/2003/InkML}"

    traces_all = [{'id': trace_tag.get('id'),
                   'coords': [[round(float(axis_coord)) if float(axis_coord).is_integer() else round(float(axis_coord) * 10000)
                               for axis_coord in coord.strip().split(' ')]
                              for coord in trace_tag.text.replace('\n', '').split(',')]}
                  for trace_tag in root.findall(doc_namespace + 'trace')]

    traces_all.sort(key=lambda trace_dict: int(trace_dict['id']))

    traceGroupWrapper = root.find(doc_namespace + 'traceGroup')

    if traceGroupWrapper is not None:
        for traceGroup in traceGroupWrapper.findall(doc_namespace + 'traceGroup'):
            label = traceGroup.find(doc_namespace + 'annotation').text

            traces_curr = []
            for traceView in traceGroup.findall(doc_namespace + 'traceView'):
                traceDataRef = int(traceView.get('traceDataRef'))
                single_trace = traces_all[traceDataRef]['coords']
                traces_curr.append(single_trace)

            traces_data.append({'label': label, 'trace_group': traces_curr})
    else:
        for trace in traces_all:
            traces_data.append({'trace_group': [trace['coords']]})

    return traces_data

def inkml2img(input_path, output_path):
    with open(output_path.split('.')[0] + '.txt', 'w') as fout:
        fout.write(get_label(input_path))

    traces = get_traces_data(input_path)
    fig, ax = plt.subplots()
    ax.invert_yaxis()
    ax.set_aspect('equal', adjustable='box')
    ax.axis('off')

    for elem in traces:
        for subls in elem['trace_group']:
            data = np.array(subls)
            x, y = zip(*data)
            ax.plot(x, y, linewidth=2, color='black')

    plt.savefig(output_path, bbox_inches='tight', dpi=100)
    plt.close(fig)
