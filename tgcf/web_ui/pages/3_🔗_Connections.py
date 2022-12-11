import time

import streamlit as st

from tgcf.config import CONFIG, Forward, read_config, write_config
from tgcf.web_ui.password import check_password
from tgcf.web_ui.utils import get_list, get_string, hide_st

CONFIG = read_config()

st.set_page_config(
    page_title="Connections",
    page_icon="🔗",
)
hide_st(st)
if check_password(st):
    add_new = st.button("Add new connection")
    if add_new:
        CONFIG.forwards.append(Forward())
        write_config(CONFIG)

    num = len(CONFIG.forwards)

    if num == 0:
        st.write(
            "No connections found. Click on Add new connection above to create one!"
        )
    else:
        tab_strings = [f"Connection {i}" for i in range(1, num + 1)]

        tabs = st.tabs(list(tab_strings))

        for i in range(num):
            with tabs[i]:
                con = i + 1

                placeholder = st.empty()

                st.write("---")
                st.write(f"Configure connection {con}")

                CONFIG.forwards[i].source = st.text_input(
                    f"Source for connection: {con}", value=CONFIG.forwards[i].source
                ).strip()
                st.write("only one source is allowed in a connection")
                CONFIG.forwards[i].dest = get_list(
                    st.text_area(
                        f"Destinations for connection: {con}",
                        value=get_string(CONFIG.forwards[i].dest),
                    )
                )
                st.write("Write destinations one item per line")

                if st.checkbox(f"Advanced options to modify connection: {con}"):
                    CONFIG.forwards[i].con_name = st.text_input(
                        "Name of this connection", value=CONFIG.forwards[i].con_name
                    )
                    if CONFIG.forwards[i].con_name:
                        placeholder.write(CONFIG.forwards[i].con_name)

                    st.info(
                        "You can untick the below checkbox to suspend this connection."
                    )
                    CONFIG.forwards[i].use_this = st.checkbox(
                        "Use this connection", value=CONFIG.forwards[i].use_this
                    )
                    if not CONFIG.forwards[i].use_this:
                        placeholder.warning("This connection is suspended.")

                    st.write("Past Mode Settings")
                    CONFIG.forwards[i].offset = int(
                        st.text_input(
                            f"Offset for connection:{con}",
                            value=str(CONFIG.forwards[i].offset),
                        )
                    )
                    CONFIG.forwards[i].end = int(
                        st.text_input(
                            f"End for connection:{con}",
                            value=str(CONFIG.forwards[i].end),
                        )
                    )

                    st.warning(
                        f"Clicking the 'Remove' button will **delete** connection {con}. This action cannot be reversed once done.",
                        icon="⚠️",
                    )

                    if st.button(f"Remove connection {con}"):
                        del CONFIG.forwards[i]
                        write_config(CONFIG)
                        st.experimental_rerun()

                st.write("---")

    if st.button("Save"):
        write_config(CONFIG)
