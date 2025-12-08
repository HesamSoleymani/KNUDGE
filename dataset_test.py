from npc_dialog.knudge_dataset import KNUDGE

dataset_wrapper = KNUDGE()

print(dataset_wrapper.dialogs['a_family_matter_00'].objectives)
print(dataset_wrapper.dialogs['a_family_matter_00'].dialog_edges)
