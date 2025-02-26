from RPCANet_Code.dulrs_package.dulrs_class.dulrs import dulrs_class

# Initial model
dulrs = dulrs_class(
    model_name="rpcanetma9", 
    model_path="/Users/yourname/My_mission/API/RPCANet_Code/result/20240519T07-24-39_rpcanetma9_nudt/best.pkl",     # Path for pretrained parameters
    use_cuda=True)

# For heatmap generation
heatmap = dulrs.heatmap(
    img_path="/Users/yourname/My_mission/API/RPCANet_Code/datasets/NUDT-SIRST/test/images/001101.png",
    data_name="NUDT-SIRST_test_images_001101",
    output_mat="./heatmap_test_2.20/mat",  # If users want to save the data as mat format. Default=None
    output_png="./heatmap_test_2.20/png"   # If users want to save the figure as png format. Default=None
)

# For lowrank calculation
lowrank_matrix = dulrs.lowrank_cal(
    img_path="/Users/yourname/My_mission/API/RPCANet_Code/datasets/test",
    model_name="rpcanetma9",
    data_name="test",
    save_dir= './mats/lowrank' # Save path for result with mat format
)

# For lowrank paint based on calculation
lowrank_matrix_draw = dulrs.lowrank_draw(
    model_name="rpcanetma9",
    data_name="test",
    mat_dir= './mats/lowrank',         
    save_dir = './mats/lowrank/figure' # Save path for result with png format
)

# For sparsity calculation
sparsity_matrix = dulrs.sparsity_cal(
    img_path="/Users/yourname/My_mission/API/RPCANet_Code/datasets/test",
    model_name="rpcanetma9",
    data_name="test",
    save_dir = './mats/sparsity'        # Save path for result with mat format
)