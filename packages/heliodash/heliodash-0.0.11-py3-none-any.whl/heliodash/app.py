import streamlit as st


def main():
    st.set_page_config(
        page_title="Heliosphere Dashboard (HelioDash)",
        page_icon="☀️",
    )

    def home():
        st.markdown(
            """
            # Heliosphere Dashboard (HelioDash)

            Heliosphere Dashboard (HelioDash) is an open-source tool for visualizing heliosphere-related data.

            ## Available Pages

            - [Positions of Planets and Spacecrafts](/Position)

            ### Sun
            - [GOES](/GOES)
            - [SOHO](/SOHO)
            - [Hinode](/Hinode)
            - [STEREO](/STEREO)
            - [PROBA-2](/PROBA2)
            - [SDO](/SDO)
            - [Parker Solar Probe](/PSP)
            - [Solar Orbiter](/SolO)

            ### Jupiter
            - [Juno](/Juno)

        """
        )

    pg = st.navigation(
        {
            "Overview": [
                st.Page(
                    home,
                    title="Home",
                    default=True,
                    icon=":material/home:",
                    url_path="",
                ),
                st.Page(
                    "dashboard/Position.py",
                    title="Positions of Planets and Spacecrafts",
                ),
            ],
            "Sun": [
                st.Page("dashboard/sun/GOES.py", title="GOES"),
                st.Page("dashboard/sun/SOHO.py", title="SOHO"),
                st.Page("dashboard/sun/Hinode.py", title="Hinode"),
                st.Page("dashboard/sun/STEREO.py", title="STEREO"),
                st.Page("dashboard/sun/PROBA2.py", title="PROBA-2"),
                st.Page("dashboard/sun/SDO.py", title="SDO"),
                st.Page("dashboard/sun/PSP.py", title="Parker Solar Probe"),
                st.Page("dashboard/sun/SolO.py", title="Solar Orbiter"),
            ],
            "Jupiter": [
                st.Page("dashboard/jupiter/Juno.py", title="Juno"),
            ],
        }
    )

    pg.run()


if __name__ == "__main__":
    main()
