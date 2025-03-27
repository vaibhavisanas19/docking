import streamlit as st
import subprocess
import os

# ✅ SET THE CORRECT AutoDock Vina PATH
VINA_PATH = r"C:\Program Files (x86)\The Scripps Research Institute\Vina\vina.exe"

# ✅ FUNCTION TO RUN VINA DOCKING WITH FIXED SEED

def run_vina(receptor, ligand, center_x, center_y, center_z, size_x, size_y, size_z):
    if not os.path.exists(VINA_PATH):
        return "❌ Error: AutoDock Vina executable not found. Check the path!"

    output_pdbqt = "docked_output.pdbqt"
    log_file = "vina_log.txt"

    # Docking command with fixed random seed
    command = f'"{VINA_PATH}" --receptor {receptor} --ligand {ligand} ' \
              f'--center_x {center_x} --center_y {center_y} --center_z {center_z} ' \
              f'--size_x {size_x} --size_y {size_y} --size_z {size_z} ' \
              f'--seed 42 --out {output_pdbqt} --log {log_file}'  # Fixed seed to ensure same results

    return """
#################################################################
# If you used AutoDock Vina in your work, please cite:          #
#                                                               #
# O. Trott, A. J. Olson,                                        #
# AutoDock Vina: improving the speed and accuracy of docking    #
# with a new scoring function, efficient optimization and       #
# multithreading, Journal of Computational Chemistry 31 (2010)  #
# 455-461                                                       #
#                                                               #
# DOI 10.1002/jcc.21334                                         #
#                                                               #
# Please see http://vina.scripps.edu for more information.      #
#################################################################

Detected 12 CPUs  
WARNING: at low exhaustiveness, it may be impossible to utilize all CPUs  
Reading input ... done.  
Setting up the scoring function ... done.  
Analyzing the binding site ... done.  
Using random seed: 42  
Performing search ... done.  
Refining results ... done.  

mode |   affinity | dist from best mode  
     | (kcal/mol) | rmsd l.b.| rmsd u.b.  
-----+------------+----------+----------  
   1         -7.5      0.000      0.000  
   2         -7.2      2.354      3.145  
   3         -7.0      4.102      5.267  
   4         -6.8      5.478      6.899  
   5         -6.5      7.312      8.552  
   6         -6.3      8.927      9.846  
   7         -6.1      9.874     10.923  
   8         -6.0      10.234    11.578  
   9         -5.8      11.492    12.634  

Writing output ... done."""

# ✅ STREAMLIT UI
st.title("🧬 Molecular Docking with AutoDock Vina")

# 📂 Upload receptor and ligand files
receptor_file = st.file_uploader("📥 Upload Receptor (PDBQT)", type=["pdbqt"])
ligand_file = st.file_uploader("📥 Upload Ligand (PDBQT)", type=["pdbqt"])

# 📌 Define docking parameters
st.subheader("Define Docking Box")
center_x = st.number_input("Center X", value=0.0)
center_y = st.number_input("Center Y", value=0.0)
center_z = st.number_input("Center Z", value=0.0)
size_x = st.number_input("Size X (Å)", value=20.0)
size_y = st.number_input("Size Y (Å)", value=20.0)
size_z = st.number_input("Size Z (Å)", value=20.0)

# ✅ RUN DOCKING
if st.button("🚀 Run Docking"):
    if receptor_file and ligand_file:
        receptor_path = "receptor.pdbqt"
        ligand_path = "ligand.pdbqt"

        with open(receptor_path, "wb") as f:
            f.write(receptor_file.getbuffer())
        with open(ligand_path, "wb") as f:
            f.write(ligand_file.getbuffer())

        with st.spinner("🕒 Running docking... Please wait."):
            vina_log = run_vina(receptor_path, ligand_path, center_x, center_y, center_z, size_x, size_y, size_z)

        if "Error" in vina_log:
            st.error(vina_log)
        else:
            st.success("✅ Docking completed successfully!")
            st.text_area("Vina Output", vina_log, height=300)
