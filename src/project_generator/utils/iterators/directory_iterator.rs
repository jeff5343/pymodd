use crate::game_data::directory::{Directory, DirectoryItem, Script};

impl Directory {
    pub fn iter_flattened(&self) -> DirectoryIterator {
        DirectoryIterator::new(self)
    }
}

pub struct DirectoryIterator<'a> {
    stack: Vec<DirectoryIterItem<'a>>,
}

impl<'a> DirectoryIterator<'a> {
    fn new(directory: &'a Directory) -> DirectoryIterator<'a> {
        DirectoryIterator {
            stack: directory
                .children
                .iter()
                .map(|directory_item| DirectoryIterItem::from(directory_item))
                .collect(),
        }
    }
}

/// Preforms a pre-order traversal on the directory
impl<'a> Iterator for DirectoryIterator<'a> {
    type Item = DirectoryIterItem<'a>;

    fn next(&mut self) -> Option<Self::Item> {
        if self.stack.len() == 0 {
            return None;
        }

        let item = self.stack.remove(0);
        if let DirectoryIterItem::StartOfDirectory(directory) = item {
            // chain DirectoryEnd on to the end of the directory's children
            self.stack.splice(
                ..0,
                directory
                    .children
                    .iter()
                    .map(|directory_item| DirectoryIterItem::from(directory_item))
                    .chain([DirectoryIterItem::DirectoryEnd]),
            );
        }
        Some(item)
    }
}

pub enum DirectoryIterItem<'a> {
    StartOfDirectory(&'a Directory),
    Script(&'a Script),
    DirectoryEnd,
}

impl<'a> DirectoryIterItem<'a> {
    fn from(directory_item: &DirectoryItem) -> DirectoryIterItem {
        match directory_item {
            DirectoryItem::Directory(directory) => DirectoryIterItem::StartOfDirectory(&directory),
            DirectoryItem::Script(script) => DirectoryIterItem::Script(&script),
        }
    }
}
