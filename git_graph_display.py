import tempfile

import graphviz

import git_graph as gg


full_option = 'hlactbr'


def display_git_graph(path, option=None, temp=False):
    display(gg.GitGraph(path), option, temp)


def display(git_graph, option=None, temp=False):
    dot_graph = build_dot_graph(git_graph.build_graph(), option)
    if temp:
        dot_graph.view(tempfile.mktemp('auto.dot'))
    else:
        dot_graph.render('auto.dot', view=False)


def build_dot_graph(git_graph, option=None):
    if not option:
        option = full_option
    node_set = filter_nodes(git_graph, option)
    dot_graph = graphviz.Digraph(name='auto', format='png',
                             graph_attr={'bgcolor': 'transparent'},
                             node_attr={'style': 'filled', 'fixedsize': 'true', 'width': '0.95'})
    if 'h' in option:
        for h in git_graph.local_head:
            dot_graph.node(h[:7], fillcolor="lightblue")
            for e in git_graph.local_head[h]:
                if e in node_set:
                    dot_graph.edge(h[:7], e[:7])
    if 'r' in option:
        for r in git_graph.remote_branches:
            dot_graph.node(r[:7], fillcolor="cyan")
            for e in git_graph.remote_branches[r]:
                if e in node_set:
                    dot_graph.edge(r[:7], e[:7])
    if 'l' in option:
        for l in git_graph.local_branches:
            dot_graph.node(l[:7], fillcolor="green")
            for e in git_graph.local_branches[l]:
                if e in node_set:
                    dot_graph.edge(l[:7], e[:7])
    if 'a' in option:
        for a in git_graph.tags:
            dot_graph.node(a[:7], fillcolor="#ff0022")
            for e in git_graph.tags[a]:
                if e in node_set:
                    dot_graph.edge(a[:7], e[:7])
    if 'a' in option:
        for a in git_graph.annotated_tags:
            dot_graph.node(a[:7], fillcolor="#ff6622")
            for e in git_graph.annotated_tags[a]:
                if e in node_set:
                    dot_graph.edge(a[:7], e[:7])
    if 'c' in option:
        for c in git_graph.commits:
            dot_graph.node(c[:7], fillcolor="#ffbb22")
            for e in git_graph.commits[c]:
                if e in node_set:
                    dot_graph.edge(c[:7], e[:7])
    if 't' in option:
        for t in git_graph.trees:
            dot_graph.node(t[:7], fillcolor="#ffccbb")
            for e in git_graph.trees[t]:
                if e[0] in node_set:
                    dot_graph.edge(t[:7], e[0][:7])
    if 'b' in option:
        for b in git_graph.blobs:
            dot_graph.node(b[:7], fillcolor="#ffdd33")
    return dot_graph


def filter_nodes(git_graph, option=None):
    if not option:
        option = full_option
    node_set = set()
    if 'h' in option:
        node_set.update(git_graph.local_head)
    if 'l' in option:
        node_set.update(git_graph.local_branches)
    if 'a' in option:
        node_set.update(git_graph.tags)
        node_set.update(git_graph.annotated_tags)
    if 'c' in option:
        node_set.update(git_graph.commits)
    if 't' in option:
        node_set.update(git_graph.trees)
    if 'b' in option:
        node_set.update(git_graph.blobs)
    return node_set
