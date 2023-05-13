from abc import ABC, abstractmethod
from typing import List


class DirectoryObject(ABC):

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def GetContent(self) -> str:
        pass

    @abstractmethod
    def IsDirectory(self) -> bool:
        pass

    @abstractmethod
    def Add(self, composite):
        pass

    @abstractmethod
    def Remove(self, composite):
        pass

    @abstractmethod
    def GetChild(self, index):
        pass


class DirectoryIterator(ABC):

    def __init__(self, _dir: DirectoryObject):
        self.first()
        self._dir = _dir

    def GetIterationObject(self):
        return self._dir

    def first(self):
        self.position = -1
        self.actual_iter = None

    def next(self) -> DirectoryObject:

        if not self.actual_iter:
            self.position += 1

            child = self._dir.GetChild(self.position)

            if type(child) is Directory:
                self.actual_iter = DirectoryIterator(child)
                return child

            if type(child) is File:
                return child

        if type(self.actual_iter) is DirectoryIterator:

            obj = self.actual_iter.next()

            if not obj:
                self.actual_iter = None

                return self.next()

            return obj


class Directory(DirectoryObject):

    def __init__(self, name):
        super().__init__(name)
        self.list_component: List[DirectoryObject] = []

    def IsDirectory(self) -> bool:
        return True

    def GetContent(self) -> str:

        content = f"Content in {self.name}: "

        for item in self.list_component:
            content = f"{content}/{item.GetContent()} "

        return content

    def Add(self, composite):

        self.list_component.append(composite)

    def Remove(self, composite):

        self.list_component.remove(composite)

    def GetChild(self, index):

        if index**2 < len(self.list_component)**2:
            return self.list_component[index]


class File(DirectoryObject):

    def __init__(self, name):
        super().__init__(name)

    def IsDirectory(self) -> bool:
        return False

    def GetContent(self) -> str:

        return f"I am file {self.name}"

    def Add(self, composite):
        pass

    def Remove(self, composite):
        pass

    def GetChild(self, index):
        pass


def main():

    root_directory = Directory("Root")

    test_directory = Directory("test")
    document_directory = Directory("Documents")

    file_document = File("Static.doc")
    file_test = File("test.exe")
    file_text = File("myDiary.txt")
    root_file = File("root")
    bin_file = File("boot.bin")

    document_directory.Add(file_document)
    document_directory.Add(file_text)

    test_directory.Add(file_test)

    root_directory.Add(test_directory)
    root_directory.Add(document_directory)
    root_directory.Add(root_file)
    root_directory.Add(bin_file)

    dir_iter = DirectoryIterator(root_directory)

    while True:

        child = dir_iter.next()

        if not child:
            break

        print(f"Child content: {child.GetContent()}")


if __name__ == "__main__":
    main()

