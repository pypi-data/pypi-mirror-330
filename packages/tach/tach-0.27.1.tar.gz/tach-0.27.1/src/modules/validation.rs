use std::collections::{HashMap, HashSet};

use crate::config::root_module::{RootModuleTreatment, ROOT_MODULE_SENTINEL_TAG};
use crate::config::utils::global_visibility;
use crate::config::ModuleConfig;
use petgraph::algo::kosaraju_scc;
use petgraph::graphmap::DiGraphMap;

use super::error::{ModuleTreeError, VisibilityErrorInfo};

pub fn find_duplicate_modules(modules: &[ModuleConfig]) -> Vec<&String> {
    let mut duplicate_module_paths = Vec::new();
    let mut seen: HashMap<&str, &ModuleConfig> = HashMap::new();

    for module in modules {
        match seen.get(module.path.as_str()) {
            Some(other_module) => {
                if !other_module.overwriteable_by(module) {
                    duplicate_module_paths.push(&module.path);
                }
            }
            None => {
                seen.insert(module.path.as_str(), module);
            }
        }
    }

    duplicate_module_paths
}

pub fn visibility_matches_module_path(visibility: &str, module_path: &str) -> bool {
    // If visibility pattern is exactly '*', any module path matches
    if visibility == "*" {
        return true;
    }

    let visibility_components: Vec<&str> = visibility.split('.').collect();
    let module_components: Vec<&str> = module_path.split('.').collect();

    // If the number of components doesn't match, return false
    if visibility_components.len() != module_components.len() {
        return false;
    }

    // Compare each component
    visibility_components
        .iter()
        .zip(module_components.iter())
        .all(|(vis_comp, mod_comp)| *vis_comp == "*" || *vis_comp == *mod_comp)
}

pub fn find_visibility_violations(modules: &[ModuleConfig]) -> Vec<VisibilityErrorInfo> {
    let mut visibility_by_path: HashMap<String, Vec<String>> = HashMap::new();
    let mut globally_visible_paths: HashSet<String> = HashSet::new();

    let global_vis = global_visibility();
    modules.iter().for_each(|module| {
        if module.visibility == global_vis {
            globally_visible_paths.insert(module.mod_path());
        } else {
            visibility_by_path.insert(module.mod_path(), module.visibility.clone());
        }
    });

    let mut results: Vec<VisibilityErrorInfo> = Vec::new();
    for module in modules.iter() {
        for dependency_config in module.dependencies_iter() {
            if let Some(visibility) = visibility_by_path.get(&dependency_config.path) {
                // check if visibility of this dependency doesn't match the current module
                if !visibility.iter().any(|visibility_pattern| {
                    visibility_matches_module_path(visibility_pattern, &module.mod_path())
                }) {
                    results.push(VisibilityErrorInfo {
                        dependent_module: module.mod_path(),
                        dependency_module: dependency_config.path.clone(),
                        visibility: visibility.clone(),
                    })
                }
            }
        }
    }

    results
}

pub fn find_modules_with_cycles(modules: &[ModuleConfig]) -> Vec<&String> {
    let mut graph = DiGraphMap::new();

    // Add nodes
    for module in modules {
        graph.add_node(&module.path);
    }

    // Add dependency edges
    for module in modules {
        for dependency in module.dependencies_iter() {
            graph.add_edge(&module.path, &dependency.path, None::<()>);
        }
    }

    // Find strongly connected components (SCCs)
    let sccs = kosaraju_scc(&graph);

    // Filter SCCs to find cycles
    let mut modules_with_cycles = Vec::new();
    for scc in sccs {
        if scc.len() > 1 {
            modules_with_cycles.extend(scc);
        }
    }

    modules_with_cycles
}

pub fn validate_root_module_treatment(
    root_module_treatment: RootModuleTreatment,
    modules: &[ModuleConfig],
) -> Result<(), ModuleTreeError> {
    match root_module_treatment {
        RootModuleTreatment::Allow | RootModuleTreatment::Ignore => Ok(()),
        RootModuleTreatment::Forbid => {
            let root_module_violations: Vec<String> = modules
                .iter()
                .filter_map(|module| {
                    if module.path == ROOT_MODULE_SENTINEL_TAG
                        || module
                            .dependencies_iter()
                            .any(|dep| dep.path == ROOT_MODULE_SENTINEL_TAG)
                    {
                        return Some(module.path.clone());
                    }
                    None
                })
                .collect();

            if root_module_violations.is_empty() {
                Ok(())
            } else {
                Err(ModuleTreeError::RootModuleViolation(format!(
                    "The root module ('{}') is forbidden, but was found in module configuration for modules: {}.",
                    ROOT_MODULE_SENTINEL_TAG,
                    root_module_violations.into_iter().map(|module| format!("'{}'", module)).collect::<Vec<_>>().join(", ")
                )))
            }
        }
        RootModuleTreatment::DependenciesOnly => {
            let root_module_violations: Vec<String> = modules
                .iter()
                .filter_map(|module| {
                    if module
                        .dependencies_iter()
                        .any(|dep| dep.path == ROOT_MODULE_SENTINEL_TAG)
                    {
                        return Some(module.path.clone());
                    }
                    None
                })
                .collect();

            if root_module_violations.is_empty() {
                Ok(())
            } else {
                Err(ModuleTreeError::RootModuleViolation(format!(
                    "The root module ('{}') is set to allow dependencies only, but was found as a dependency in: {}.",
                    ROOT_MODULE_SENTINEL_TAG,
                    root_module_violations.into_iter().map(|module| format!("'{}'", module)).collect::<Vec<_>>().join(", ")
                )))
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::{parsing::config::parse_project_config, tests::fixtures::example_dir};
    use rstest::rstest;
    use std::path::PathBuf;
    #[rstest]
    fn test_valid_circular_dependencies(example_dir: PathBuf) {
        let project_config = parse_project_config(example_dir.join("valid/tach.toml"));
        assert!(project_config.is_ok());
        let (project_config, _) = project_config.unwrap();
        let modules = project_config.all_modules().cloned().collect::<Vec<_>>();
        let modules_with_cycles = find_modules_with_cycles(&modules);
        assert!(modules_with_cycles.is_empty());
    }

    #[rstest]
    fn test_cycles_circular_dependencies(example_dir: PathBuf) {
        let project_config = parse_project_config(example_dir.join("cycles/tach.toml"));
        assert!(project_config.is_ok());
        let (project_config, _) = project_config.unwrap();
        let modules = project_config.all_modules().cloned().collect::<Vec<_>>();
        let module_paths = find_modules_with_cycles(&modules);
        assert_eq!(module_paths, ["domain_one", "domain_two", "domain_three"]);
    }
}
