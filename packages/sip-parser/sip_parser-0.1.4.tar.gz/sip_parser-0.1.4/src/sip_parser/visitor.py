""" visitor.py """

from arpeggio import PTNodeVisitor
from collections import namedtuple

Scenario = namedtuple('Scenario', 'name classes')
ClassModelPopulation = namedtuple('ClassModelPopulation', 'header population')

class ScenarioVisitor(PTNodeVisitor):

    # Root
    @classmethod
    def visit_si_population(cls, node, children):
        """
        EOL* scenario (class_def instance_block)+ EOF
        """
        scenario_name = children[0]
        cdict = dict()
        # The first child element is the scenario name, we we excludd that
        # and process columns (c) and instances (i) two at a time
        it = iter(children[1:])  # Create an iterator and then zip it to get non-overlapping list element pairs
        for c, i in zip(it, it):
            cname = c[0]
            header = c[1]
            # refs = c[1]['refs']
            pop = list(i['instances'])
            cdict[cname] = ClassModelPopulation(header=header, population=pop)
        return Scenario(name=scenario_name, classes=cdict)

    @classmethod
    def visit_scenario(cls, node, children):
        """ scenario_name block_end """
        return children[0]

    @classmethod
    def visit_class_def(cls, node, children):
        """ class_name class_attrs block_end """
        return children

    @classmethod
    def visit_class_attrs(cls, node, children):
        """ col_name (' | ' col_name)* block_end """
        # attrs = [c for c in children if isinstance(c, str)]
        # refs = next((c for c in children if isinstance(c, list)), None)
        # items = {"attr": attrs, "refs": refs}
        return children

        # return items

    @classmethod
    def visit_col_name(cls, node, children):
        """ rnum_list / icaps_name """
        # items = {k: v for d in children for k, v in d.items()}
        # return items
        return children[0]

    @classmethod
    def visit_ref_list(cls, node, children):
        """ ref (', ' ref)* """
        # items = {k: v for d in children for k, v in d.items()}
        # return items
        return children

    @classmethod
    def visit_ref(cls, node, children):
        """ rnum '>' icaps_name """
        # items = {k: v for d in children for k, v in d.items()}
        # return items
        return {'rnum': children[0], 'to class':children[1]}


    @classmethod
    def visit_instance_block(cls, node, children):
        """ row* block_end """
        # name = ''.join(children)
        # return {'name': name }
        return {'instances': children}

    @classmethod
    def visit_row(cls, node, children):
        """ (word SP+)? '{ ' val (SP+ val)* ' }' EOL """
        alias = children.results.get('word')
        alias = alias[0] if alias else None
        return { 'alias': alias, 'row': children.results['val'] }

    @classmethod
    def visit_brace_val(cls, node, children):
        """ '[' ival ']' """
        return children[0]

    @classmethod
    def visit_at_val(cls, node, children):
        """ '@' word """
        return { 'ref to': children[0] }

    @classmethod
    def visit_val(cls, node, children):
        """ row_value (', ' row_value)* """
        return children[0]

    @classmethod
    def visit_class_name(cls, node, children):
        """ icaps_name """
        return children[0]
        # return { 'class': children[0] }

    @classmethod
    def visit_icaps_name(cls, node, children):
        """
        word (delim word)*
        """
        name = ''.join(children)
        return name

    @classmethod
    def visit_EOL(cls, node, children):
        """
        SP* COMMENT? '\n'

        end of line: Spaces, Comments, blank lines, whitespace we can omit from the parser result
        """
        return None

    @classmethod
    def visit_SP(cls, node, children):
        """ ' '  Single space character (SP) """
        return None
