use crate::components::iu::core::IUCoreError;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// Datastructure that implements IULinks based on a HashMap.
#[derive(Default, Debug, Serialize, Deserialize, Clone)]
pub struct IULinks {
    pub link_map: HashMap<String, Vec<String>>,
}

impl IULinks {
    pub fn add_target_to_link(&mut self, link_name: &str, target: impl Into<String>) {
        if let Some(v) = self.link_map.get_mut(link_name) {
            v.push(target.into());
        } else {
            self.link_map
                .insert(link_name.to_string(), vec![target.into()]);
        }
    }

    pub fn remove_target_from_link(
        &mut self,
        link_name: &str,
        target: &str,
    ) -> Result<(), IUCoreError> {
        if let Some(v) = self.link_map.get_mut(link_name) {
            if let Some(i) = v.iter().position(|x| x == target) {
                v.remove(i);
                if v.is_empty() {
                    self.remove_link(link_name)?;
                }
                Ok(())
            } else {
                Err(IUCoreError::LinkTargetNotFound)
            }
        } else {
            Err(IUCoreError::LinkNotFound)
        }
    }

    pub fn remove_link(&mut self, link_name: &str) -> Result<(), IUCoreError> {
        self.link_map
            .remove(link_name)
            .ok_or(IUCoreError::LinkNotFound)
            .map(|_| ())
    }
}

#[cfg(test)]
mod tests {
    use crate::components::iu::core::IUCoreError;
    use crate::components::iu::links::IULinks;
    use std::collections::HashMap;

    #[test]
    fn iu_link_test() {
        let mut iu_links = IULinks::default();
        iu_links.add_target_to_link("grounded-in", "abc");
        iu_links.add_target_to_link("grounded-in", "def");
        iu_links.add_target_to_link("grounded-in", "fff");
        iu_links.add_target_to_link("joy", "fff");
        iu_links.add_target_to_link("joy", "ddd");

        assert_eq!(
            iu_links.link_map,
            HashMap::from([
                (
                    "grounded-in".to_string(),
                    vec!["abc".to_string(), "def".to_string(), "fff".to_string()]
                ),
                (
                    "joy".to_string(),
                    vec!["fff".to_string(), "ddd".to_string()]
                )
            ])
        );

        iu_links
            .remove_target_from_link("grounded-in", "def")
            .unwrap();
        assert_eq!(
            iu_links.remove_target_from_link("grounded-in", "def"),
            Err(IUCoreError::LinkTargetNotFound)
        );
        assert_eq!(
            iu_links.remove_target_from_link("grounded-in", "ggg"),
            Err(IUCoreError::LinkTargetNotFound)
        );
        assert_eq!(
            iu_links.remove_target_from_link("ggg", "gdddd-in"),
            Err(IUCoreError::LinkNotFound)
        );

        iu_links
            .remove_target_from_link("grounded-in", "abc")
            .unwrap();
        iu_links
            .remove_target_from_link("grounded-in", "fff")
            .unwrap();

        assert_eq!(
            iu_links.remove_link("grounded-in"),
            Err(IUCoreError::LinkNotFound)
        );

        iu_links.remove_link("joy").unwrap();

        assert_eq!(iu_links.link_map, HashMap::default())
    }
}
