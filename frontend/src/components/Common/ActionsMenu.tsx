import {Button, Menu, MenuButton, MenuItem, MenuList, useDisclosure,} from "@chakra-ui/react"
import {BsThreeDotsVertical} from "react-icons/bs"
import {FiEdit, FiTrash} from "react-icons/fi"

import type {ConversationPublic, UserPublic} from "../../client"
import EditUser from "../Admin/EditUser"
import Delete from "./DeleteAlert"
import {useNavigate} from "@tanstack/react-router";

interface ActionsMenuProps {
  type: string
  value: ConversationPublic | UserPublic
  disabled?: boolean
  onDeleteSuccess: () => void
}

const ActionsMenu = ({ type, value, disabled, onDeleteSuccess }: ActionsMenuProps) => {
  const navigate = useNavigate()
  const editUserModal = useDisclosure()
  const deleteModal = useDisclosure()

  return (
    <>
      <Menu>
        <MenuButton
          isDisabled={disabled}
          as={Button}
          rightIcon={<BsThreeDotsVertical />}
          variant="unstyled"
        />
        <MenuList>
          { type === "Conversation" &&
          <MenuItem
            onClick={() => navigate({ to: '/', search: { conversation_id: value.id }})}
            icon={<FiEdit fontSize="16px" />}
          >
            Continue {type}
          </MenuItem>
          }
          { type === "User" &&
          <MenuItem
            onClick={editUserModal.onOpen}
            icon={<FiEdit fontSize="16px" />}
          >
            Edit {type}
          </MenuItem>
          }
          <MenuItem
            onClick={deleteModal.onOpen}
            icon={<FiTrash fontSize="16px" />}
            color="ui.danger"
          >
            Delete {type}
          </MenuItem>
        </MenuList>
        {type === "User" && (
          <EditUser
            user={value as UserPublic}
            isOpen={editUserModal.isOpen}
            onClose={editUserModal.onClose}
          />
        )}
        <Delete
          type={type}
          id={value.id}
          isOpen={deleteModal.isOpen}
          onClose={deleteModal.onClose}
          onDeleteSuccess={onDeleteSuccess}
        />
      </Menu>
    </>
  )
}

export default ActionsMenu
