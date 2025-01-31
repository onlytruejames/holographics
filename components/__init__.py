class VariableManager:
    def __init__(this, name, datatype, value, description=None):
        this.name = name
        this.datatype = datatype
        this.description = description
        this.value = value