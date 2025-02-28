use rmp_serde;
use serde::{Deserialize, Serialize};
use serde_json;
use thiserror::Error;
use uuid::Uuid;

use crate::components::iu::links::IULinks;
use crate::VoidOrAsyncError;

/// Core of Incremental Unit. Used together with IU (as a Wrapper for Callbacks).
///
/// Essential unit for information Exchange between Components.
///
#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct IUCore {
    ///  string representing the broad category of data, e.g. "asrresults" for transmitting the results of ASR
    pub category: String,
    /// globally unique identifier. Used for equality checks and the Backend Channel.
    pub uid: String,
    /// Output Buffer that "owns" the IU. Used to identify events that should manipulate the iu
    pub owner_buffer_uid: Option<String>,
    /// Is the owner committed to the IU
    pub is_committed: bool,
    /// links of the IU adding new keys creates a list
    pub links: IULinks,
    /// actual message content of the IU
    pub payload: serde_json::Value,
    pub component_name: String,
}

impl IUCore {
    pub fn new(
        category: impl Into<String>,
        component_name: impl Into<String>,
        owner_buffer_uid: Option<String>,
        payload: serde_json::Value,
        uid: impl Into<String>,
    ) -> Self {
        let category = category.into();
        let component_name = component_name.into();
        let uid = uid.into();
        Self {
            uid,
            owner_buffer_uid,
            category,
            payload,
            component_name,
            ..Default::default()
        }
    }

    /// Commits this IU. Can (or should) only be done by the owner of the IU.
    /// Is checked via a passed id, which might make misuse possible.
    ///
    /// Returns IU::CommittedByNonOwner if buffer_id is not the owner.
    pub async fn commit(&mut self, buffer_id: &str) -> VoidOrAsyncError {
        let owning_buffer = self
            .owner_buffer_uid
            .as_ref()
            .ok_or(IUCoreError::OwningBufferNotSet)?
            .to_string();
        if buffer_id == owning_buffer {
            self.is_committed = true;
            Ok(())
        } else {
            Err(Box::new(IUCoreError::CommittedByNonOwner {
                committed_by: buffer_id.to_string(),
                iu_id: self.uid.to_string(),
                owner: owning_buffer,
            }))
        }
    }

    /// adds a target to a link. Target should be an IU uid. If the link doesn't exist, will be created.
    pub fn add_target_to_link(&mut self, link_name: &str, target: impl Into<String>) {
        self.links.add_target_to_link(link_name, target);
    }

    /// Removes a target from a link. Target should be an IU uid. If the link would have no more
    /// targets after removal, it will be removed as well.
    ///
    /// Can return respective errors, if the target or link is not found.
    pub fn remove_target_from_link(
        &mut self,
        link_name: &str,
        target: &str,
    ) -> Result<(), IUCoreError> {
        self.links.remove_target_from_link(link_name, target)
    }

    pub fn remove_link(&mut self, link_name: &str) -> Result<(), IUCoreError> {
        self.links.remove_link(link_name)
    }

    pub fn get_bytes(&self) -> Vec<u8> {
        let mut buf = Vec::new();
        self.serialize(&mut rmp_serde::Serializer::new(&mut buf))
            .unwrap();
        buf
    }
}

impl PartialEq<Self> for IUCore {
    fn eq(&self, other: &Self) -> bool {
        self.uid == other.uid
    }
}

impl Default for IUCore {
    fn default() -> Self {
        let uid = Uuid::new_v4().to_string();
        let owner_buffer_uid = None;
        Self {
            category: "".to_string(),
            uid,
            owner_buffer_uid,
            is_committed: false,
            links: Default::default(),
            payload: Default::default(),
            component_name: "".to_string(),
        }
    }
}

#[derive(Error, Debug, Eq, PartialEq)]
pub enum IUCoreError {
    #[error("{committed_by} tried to commit IU {iu_id}, but the owner is {owner}.")]
    CommittedByNonOwner {
        committed_by: String,
        iu_id: String,
        owner: String,
    },
    #[error("Link not found")]
    LinkNotFound,
    #[error("Target in Link not found")]
    LinkTargetNotFound,
    #[error("Committed IUs can't be modified")]
    ValueChangeForCommittedIU,
    #[error("Owning Buffer not set")]
    OwningBufferNotSet,
}

#[cfg(test)]
mod tests {
    use crate::components::iu::core::IUCore;
    use crate::components::iu::*;

    #[test]
    fn iu_core_test() {
        let iu: IUCore = IUCore::new(
            "chicken",
            "IUCoreTest",
            Some(Uuid::new_v4().to_string()),
            serde_json::Value::default(),
            Uuid::new_v4().to_string(),
        );
        assert_eq!(iu.uid.to_string().len(), 36);
    }
}
