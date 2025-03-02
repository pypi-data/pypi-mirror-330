class Selector(object):
    def __init__(self,
                 tag: str = "*",
                 Id: str = "",
                 class_: str = "",
                 not_class: str = "",
                 contains: str = "",
                 attrs: dict = None,
                 not_attrs: list = None,
                 starts_with: dict = None,
                 ends_with: dict = None,
                 nth_child: int = None,
                 last_child: bool = False,
                 direct_parent: str = "",
                 any_parent: str = ""):

        '''

        :param tag: The HTML tag to select (default is "*").
        :param Id: The ID attribute of the element.
        :param class_: The class name to match.
        :param not_class: Excludes elements with this class.
        :param contains: Matches elements containing this text.
        :param attrs: Dictionary of attributes to match (e.g., {"name": "value"}).
        :param not_attrs: List of attributes that must not be present.
        :param starts_with: Dictionary of attributes that must start with a value.
        :param ends_with: Dictionary of attributes that must end with a value.
        :param nth_child: Selects the nth child of its parent.
        :param last_child: If True, selects only the last child.
        :param direct_parent: Selects elements with this direct parent.
        :param any_parent: Selects elements with this parent at any level.
        '''

        self.Id = Id
        self.class_ = class_
        self.not_class = not_class
        self.contains = contains
        self.tag = tag
        self.attrs = attrs or {}
        self.not_attrs = not_attrs or []
        self.starts_with = starts_with or {}
        self.ends_with = ends_with or {}
        self.nth_child = nth_child
        self.last_child = last_child
        self.direct_parent = direct_parent
        self.any_parent = any_parent

        self.xpath = self.create_xpath()
        self.css = self.create_css()


    def create_xpath(self, position: int = None, last: bool = False) -> str:
        conditions = []

        if self.Id:
            conditions.append(f"@id='{self.Id}'")

        if self.class_:
            conditions.append(f"contains(concat(' ', normalize-space(@class), ' '), ' {self.class_} ')")

        if self.not_class:
            conditions.append(f"not(contains(concat(' ', normalize-space(@class), ' '), ' {self.not_class} '))")

        if self.contains:
            conditions.append(f"contains(text(), '{self.contains}')")

        for key, value in self.attrs.items():
            conditions.append(f"@{key}='{value}'")

        for attr in self.not_attrs:
            conditions.append(f"not(@{attr})")

        for key, value in self.starts_with.items():
            conditions.append(f"starts-with(@{key}, '{value}')")

        for key, value in self.ends_with.items():
            conditions.append(f"substring(@{key}, string-length(@{key}) - string-length('{value}') + 1) = '{value}'")

        position_str = f"[position()={position}]" if position else ""
        last_str = "[last()]" if last else ""

        xpath = f"//{self.tag}" + (f"[{' and '.join(conditions)}]" if conditions else "") + position_str + last_str

        if self.direct_parent:
            xpath = f"//{self.direct_parent}/{xpath}"

        if self.any_parent:
            xpath = f"//{self.any_parent}//{xpath}"

        return xpath


    def create_css(self) -> str:
        selectors = []

        if self.any_parent:
            selectors.append(f"{self.any_parent} ")

        if self.direct_parent:
            selectors.append(f"{self.direct_parent} > ")

        if self.tag and self.tag != "*":
            selectors.append(self.tag)

        if self.Id:
            selectors.append(f"#{self.Id}")

        if self.class_:
            selectors.append("." + ".".join(self.class_.split()))

        attr_selectors = []
        for key, value in self.attrs.items():
            attr_selectors.append(f"[{key}='{value}']")

        for attr in self.not_attrs:
            attr_selectors.append(f":not([{attr}])")

        if self.not_class:
            attr_selectors.append(f":not(.{self.not_class.replace(' ', '.').strip()})")

        for key, value in self.starts_with.items():
            attr_selectors.append(f"[{key}^='{value}']")

        for key, value in self.ends_with.items():
            attr_selectors.append(f"[{key}$='{value}']")

        if self.nth_child:
            attr_selectors.append(f":nth-child({self.nth_child})")

        if self.last_child:
            attr_selectors.append(":last-child")

        css = "".join(selectors) + "".join(attr_selectors)

        if self.contains:
            css += f":contains('{self.contains}')"  # Note: CSS does not support :contains, but it can be used with query.

        return css


    def __str__(self):
        return self.css


    def __repr__(self):
        return f"<Selector {self.css}>"