pub struct PyprojectTomlFile {}

impl PyprojectTomlFile {
    pub fn build_content() -> String {
        return format!(
            "[tool.basedpyright]\n\
            reportImplicitRelativeImport = false\n\
            reportImplicitOverride = false\n\
            reportUnusedCallResult = false\n\
            reportUnannotatedClassAttribute = false\n\
            reportMissingTypeStubs = false\n\
            reportWildcardImportFromLibrary = false\n\
            reportAny = false\n"
        );
    }
}
