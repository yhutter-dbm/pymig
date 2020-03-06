class SideNavHelper():

    @staticmethod
    def reset_all_active_states(side_nav_elements):
        for side_nav_element in side_nav_elements:
            side_nav_element.reset()

        return side_nav_elements

    @staticmethod
    def set_active_side_nav_element(current_path, side_nav_elements, logger):
        side_nav_elements = SideNavHelper.reset_all_active_states(
            side_nav_elements)
        # We set the element activate which has a matching key in the side nav elements
        for side_nav_element in side_nav_elements:
            if side_nav_element.title == current_path:
                side_nav_element.active = True
                logger.info("Active side nav element is %s",
                            side_nav_element.title)
        return side_nav_elements
