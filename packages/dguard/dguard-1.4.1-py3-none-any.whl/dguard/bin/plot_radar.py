import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

def create_radar_chart(df, title, output_path):
    # if 'EER' not in df, copy 'EER_mean' as EER
    if "EER_mean" in df:
        df["EER"] = df["EER_mean"]
    # EER to float
    df["EER"] = df["EER"].astype(float)
    labels = df[
        "trials"
    ].unique()  # The axes will represent the different trials
    num_vars = len(labels)

    # Compute angle for each axis
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]  # Complete the loop
    # EER = 100-EER
    df["ACC"] = 100 - df["EER"]  # acc
    # Setup plot
    fig, ax = plt.subplots(figsize=(20, 16), subplot_kw=dict(polar=True))
    best_acc_in_each_trial = df.groupby("trials")["ACC"].max()
    xtrick_labels = [
        f"{label}\n(Score: {best_acc_in_each_trial[label]:.2f})"
        for label in labels
    ]
    plt.xticks(
        angles[:-1], xtrick_labels, fontsize=15
    )  # Set trial names as labels

    # Normalize EER values based on the maximum EER for each trial to set dynamic range on each axis
    max_eer_per_trial = df.groupby("trials")["ACC"].max()
    scaled_eer = df.apply(
        lambda x: x["ACC"] / max_eer_per_trial[x["trials"]], axis=1
    )

    # Define colors for each model
    colors = plt.cm.viridis(np.linspace(0, 1, len(df["model"].unique())))
    with open(output_path.replace(".png", ".txt"), "w") as f:
        for i, (model_name, group) in enumerate(df.groupby("model")):
            # Normalize values by the maximum EER in each trial for consistent scaling
            values = group.apply(
                lambda x: x["ACC"] / max_eer_per_trial[x["trials"]], axis=1
            ).tolist()
            values += values[:1]  # Complete the loop
            # values = 100 - values
            print(values)
            # values = [100 - x * 100 for x in values]
            if len(values) != len(angles):
                print(
                    f"Lenght of values={len(values)} != len(angles)={len(angles)}"
                )
                print(f"Skipping model {model_name} due to mismatch in data")
                continue
            model_index = f"Model {i+1}"
            ax.plot(
                angles,
                values,
                "o-",
                linewidth=2,
                label=model_index,
                color=colors[i],
            )
            f.write(f"# {model_index}: {model_name}\n")
            ax.fill(angles, values, alpha=0.25, color=colors[i])

    # ax.set_yticklabels([])
    # ax.set_rticks([])
    # Set Y axis labels to display actual EER values corresponding to each axis segment
    max_value = scaled_eer.max()
    ax.set_ylim(0.75, 1.0)  # Setting the limit
    ax.set_rlim(0.75, 1.0)  # Setting the limit
    ax.set_rticks([0.75, 1.0])  # Set five levels; adjust if needed
    # ax.set_rticks([])  # Set five levels; adjust if needed
    ax.set_yticklabels(["75% of Best Model", "Best Model"], fontsize=12)
    # ax.set_yticklabels([])

    plt.title(title, size=18, y=1.1)
    plt.legend(loc="upper right", bbox_to_anchor=(0.1, 0.1), fontsize=15)
    plt.savefig(output_path)
    plt.close()


# def create_radar_chart(df, title, output_path):
#     if 'EER_mean' in df:
#         df['EER'] = df['EER_mean']
#     df['EER'] = df['EER'].astype(float)
#     labels = df['trials'].unique()  # The axes will represent the different trials
#     num_vars = len(labels)

#     # Compute angle for each axis
#     angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
#     angles += angles[:1]  # Complete the loop
#     df['ACC'] = 100 - df['EER'] # Calculate accuracy as 100 - EER

#     # Setup plot
#     fig, ax = plt.subplots(figsize=(20, 16), subplot_kw=dict(polar=True))
#     best_acc_in_each_trial = df.groupby('trials')['ACC'].max()
#     xtrick_labels = [f"{label}\n(Score: {best_acc_in_each_trial[label]:.2f})" for label in labels]
#     plt.xticks(angles[:-1], xtrick_labels, fontsize=15)  # Set trial names as labels

#     # Normalize EER values based on the maximum EER for each trial to set dynamic range on each axis
#     max_eer_per_trial = df.groupby('trials')['ACC'].max()
#     scaled_eer = df.apply(lambda x: x['ACC'] / max_eer_per_trial[x['trials']], axis=1)

#     # Define colors for each model
#     model_names = df['model'].unique()
#     colors = plt.cm.viridis(np.linspace(0, 1, len(model_names)))
#     for i, (model_name, group) in enumerate(df.groupby('model')):
#         values = group.apply(lambda x: x['ACC'] / max_eer_per_trial[x['trials']], axis=1).tolist()
#         values += values[:1]  # Complete the loop
#         if len(values) != len(angles):
#             print(f"len(values)={len(values)} != len(angles)={len(angles)}")
#             print(f"Skipping model {model_name} due to mismatch in data")
#             continue
#         ax.plot(angles, values, 'o-', linewidth=2, label=f'Model {i+1}', color=colors[i])
#         ax.fill(angles, values, alpha=0.25, color=colors[i])

#     ax.set_ylim(0.75, 1.0)  # Setting the limit
#     ax.set_rlim(0.75, 1.0)  # Setting the limit
#     ax.set_rticks([0.75, 1.0])  # Set levels
#     ax.set_yticklabels(["75% of Best Model", "Best Model"], fontsize=12)

#     plt.title(title, size=18, y=1.1)
#     model_name_shorts = {}
#     with open(output_path.replace('.png', '.txt'), 'w') as f:
#         for _index,model_name in enumerate(model_names,1):
#             model_index = _index
#             # print(f"# Model {model_index}: {model_name}")
#             f.write(f"# Model {model_index}: {model_name}\n")
#             model_name_shorts[model_name] = f"Model {model_index}"
#         plt.legend([model_name_shorts[model_name] for model_name in model_names], loc='upper right', bbox_to_anchor=(0.1, 0.1), fontsize=15)
#         plt.savefig(output_path)
#         plt.close()


def main():
    import argparse

    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--csv_path", type=str, help="Path to the CSV file")
    parser.add_argument(
        "--output_folder", type=str, help="Path to the output folder"
    )
    args = parser.parse_args()
    csv_path = args.csv_path
    output_folder = args.output_folder

    df = pd.read_csv(csv_path)
    os.makedirs(output_folder, exist_ok=True)
    for time in df["time"].unique():
        time_data = df[df["time"] == time]
        output_path = os.path.join(
            output_folder, f"radar_chart_time_{time}.png"
        )
        create_radar_chart(
            time_data, f"Radar Chart for Time {time}", output_path
        )
        print(f"Plot saved: {output_path}")


if __name__ == "__main__":
    main()
