#!/usr/bin/env python
#
# Perform PRS calculations given and MD trajectory and a final state
# co-ordinate file
#
# Script distributed under GNU GPL 3.0
#
# Author: David Penkler
# Date: 17-11-2016

import argparse
import sys
from math import floor, log10, sqrt

import numpy as np
from lazydock_md_task import sdrms
from lazydock_md_task.cli import CLI
from lazydock_md_task.trajectory import load_trajectory
from lazydock_md_task.utils import Logger
from MDAnalysis import Universe
from tqdm import tqdm
from mbapy_lite.base import put_err, put_log


def round_sig(x, sig=2):
    return round(x,sig-int(floor(log10(x)))-1)


def trajectory_to_array(traj, totalframes, totalres):
    trajectory = np.zeros((totalframes, totalres*3))

    for row, frame in enumerate(traj):
        top = frame.topology

        col = 0
        for atom_index, atom in enumerate(top.atoms):
            if atom.name == "CA":
                trajectory[row,col:col+3] = frame.xyz[0,atom_index]*10
                col += 3

    return trajectory


def align_frame(reference_frame, alternative_frame, aln=False):
    totalres = reference_frame.shape[0]

    if aln:
        return sdrms.superpose3D(alternative_frame.reshape(totalres, 3), reference_frame, refmask=mask, targetmask=mask)[0].reshape(1, totalres*3)[0]
    else:
        return sdrms.superpose3D(alternative_frame.reshape(totalres, 3), reference_frame)[0].reshape(1, totalres*3)[0]


def calc_rmsd(reference_frame, alternative_frame, aln=False):
    if aln:
        return sdrms.superpose3D(alternative_frame, reference_frame, refmask=mask, targetmask=mask)[1]
    else:
        return sdrms.superpose3D(alternative_frame, reference_frame)[1]


def main(topology_path: str, trajectory_path: str, chain: str = None,
         initial_frame: int = 0, final_frame: int = None, step: int = 1,
         align: bool = False, perturbations: int = 250):
    put_log("Loading trajectory...\n")
    # prepare trajectory and topology
    u = Universe(topology_path, trajectory_path)
    atoms = u.select_atoms("name CA and protein")
    if chain is not None:
        atoms = atoms[atoms.chainIDs == chain]
    # extract coords
    sum_frames = (len(u.trajectory) if final_frame is None else final_frame) - initial_frame
    coords = np.zeros((len(u.trajectory), len(atoms), 3), dtype=np.float64)
    for current, _ in enumerate(tqdm(u.trajectory[initial_frame:final_frame:step],
                                     desc='Gathering coordinates', total=sum_frames, leave=False)):
        coords[current] = atoms.positions.reshape(-1, 3)
    coords = (coords * 10.).astype(np.float64)
    n_residues = u.atoms.n_residues
    initial_coords, final_coords = coords[0].copy(), coords[-1].copy()
    # align frames
    for i in tqdm(range(0, sum_frames), desc='Aligning frames', total=sum_frames, leave=False):
        coords[i] = align_frame(initial_coords, coords[i], align)
    # calculate difference between frame atoms and average atoms
    put_log("- Calculating average structure...\n")
    average_structure_1 = np.mean(coords, axis=0).reshape(n_residues, 3)
    for i in tqdm(range(0, 10), desc='Aligning to average structure', total=10, leave=False):
        for frame in range(0, sum_frames):
            aligned_mat[frame] = align_frame(average_structure_1, aligned_mat[frame], align)
        average_structure_2 = np.average(aligned_mat, axis=0).reshape(n_residues, 3)
        rmsd = calc_rmsd(average_structure_1, average_structure_2, align)
        put_log('   - %s Angstroms from previous structure\n' % str(rmsd))
        average_structure_1 = average_structure_2
        del average_structure_2
        if rmsd <= 0.000001:
            for frame in range(0, sum_frames):
                aligned_mat[frame] = align_frame(average_structure_1, aligned_mat[frame], align)
            break
    # Calculate the average structure
    put_log("Calculating difference between frame atoms and average atoms...\n")
    meanstructure = average_structure_1.reshape(n_residues*3)
    put_log('- Calculating R_mat\n')
    R_mat = np.zeros((totalframes, totalres*3))
    for frame in range(0, totalframes):
        R_mat[frame,:] = (aligned_mat[frame,:]) - meanstructure

    put_log('- Transposing\n')

    RT_mat = np.transpose(R_mat)

    RT_mat = np.mat(RT_mat)
    R_mat = np.mat(R_mat)

    put_log('- Calculating corr_mat\n')

    corr_mat = (RT_mat * R_mat)/ (totalframes-1)
    np.savetxt("corr_mat.txt", corr_mat)

    del aligned_mat
    del meanstructure
    del R_mat
    del RT_mat


    put_log('Reading initial and final PDB co-ordinates...\n')

    initial = np.zeros((totalres, 3))
    final = np.zeros((totalres, 3))

    with open(args.initial, 'r') as initial_lines:
        with open(args.final, 'r') as final_lines:

            res_index = 0
            for line_index, initial_line in enumerate(initial_lines):
                final_line = final_lines.readline()

                if line_index >= 1 and res_index < totalres:
                    initial_res = initial_line.strip().split()

                    if(len(initial_res[0]) == 4):
                        final_res = final_line.strip().split()

                        initial[res_index,] = initial_res[1:]
                        final[res_index,] = final_res[1:]
                        res_index += 1


    put_log('Calculating experimental difference between initial and final co-ordinates...\n')

    if align:
        put_log("- Using NTD alignment restrictions\n")
        final_alg = sdrms.superpose3D(final, initial, refmask=mask, targetmask=mask)[0]
    else:
        final_alg = sdrms.superpose3D(final, initial)[0]

    diffE = (final_alg-initial).reshape(totalres*3, 1)

    del final
    del final_alg


    put_log('Implementing perturbations sequentially...\n')

    perturbations = int(args.perturbations)
    diffP = np.zeros((totalres, totalres*3, perturbations))
    initial_trans = initial.reshape(1, totalres*3)

    for s in range(0, perturbations):
        for i in range(0, totalres):
            delF = np.zeros((totalres*3))
            f = 2 * np.random.random((3, 1)) - 1
            j = (i + 1) * 3

            delF[j-3] = round_sig(abs(f[0,0]), 5)* -1 if f[0,0]< 0 else round_sig(abs(f[0,0]), 5)
            delF[j-2] = round_sig(abs(f[1,0]), 5)* -1 if f[1,0]< 0 else round_sig(abs(f[1,0]), 5)
            delF[j-1] = round_sig(abs(f[2,0]), 5)* -1 if f[2,0]< 0 else round_sig(abs(f[2,0]), 5)

            diffP[i,:,s] = np.dot((delF), (corr_mat))
            diffP[i,:,s] = diffP[i,:,s] + initial_trans[0]

            if align:
                diffP[i,:,s] = ((sdrms.superpose3D(diffP[i,:,s].reshape(totalres, 3), initial, refmask=mask, targetmask=mask)[0].reshape(1, totalres*3))[0]) - initial_trans[0]
            else:
                diffP[i,:,s] = ((sdrms.superpose3D(diffP[i,:,s].reshape(totalres, 3), initial)[0].reshape(1, totalres*3))[0]) - initial_trans[0]
            del delF

    del initial_trans
    del initial
    del corr_mat


    put_log("Calculating Pearson's correlations coefficient...\n")
    # 计算DTarget的向量化版本
    diffE_reshaped = diffE.reshape(-1, 3)
    DTarget = np.linalg.norm(diffE_reshaped, axis=1)
    # 计算DIFF的向量化版本
    diffP_reshaped = diffP.reshape(totalres, totalres, 3, perturbations)
    DIFF = np.linalg.norm(diffP_reshaped, axis=2).transpose(1, 0, 2)
    del diffP  # 显式删除不再需要的数组
    # 计算RHO的向量化版本
    # 重组DIFF为二维矩阵便于批量计算
    reshaped_diff = DIFF.transpose(1, 2, 0).reshape(-1, totalres)
    dt_centered = DTarget - DTarget.mean()
    # 批量计算协方差和标准差
    diff_centered = reshaped_diff - reshaped_diff.mean(axis=1, keepdims=True)
    covariances = (diff_centered @ dt_centered) / (totalres - 1)
    std_devs = diff_centered.std(axis=1, ddof=1) * dt_centered.std(ddof=1)
    # 避免除以零（假设数据无零标准差情况）
    RHO = (covariances / std_devs).reshape(totalres, perturbations)

    maxRHO = np.zeros(totalres)
    for i in range(0, totalres):
        maxRHO[i] = np.amax(abs(RHO[i,:]))

    np.savetxt("%s.csv" % args.prefix, maxRHO, delimiter=",", header=args.prefix)

    del maxRHO



if __name__ == "__main__":
    main('/home/pcmd36/Desktop/BHM/LFH/CB1-SNP/data/7_MDS/HigherTrajAna/interactions/C2 s0 MT t2/full_md.tpr',
         '/home/pcmd36/Desktop/BHM/LFH/CB1-SNP/data/7_MDS/HigherTrajAna/interactions/C2 s0 MT t2/full_md_center.xtc',
         final_frame=100)
