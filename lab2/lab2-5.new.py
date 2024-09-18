import tkinter as tk
from tkinter import messagebox
import random


class InvalidNucleotideError(Exception):
    """Исключение, которое выбрасывается, если в строке содержатся недопустимые символы."""
    pass


class DNA:
    def __init__(self, sequence):
        self.sequence = sequence.upper()
        self._validate_sequence('ATGC')

    def _validate_sequence(self, allowed_bases):
        for base in self.sequence:
            if base not in allowed_bases:
                raise InvalidNucleotideError(f"Недопустимый нуклеотид '{base}' в последовательности ДНК.")

    def to_list(self):
        complement = {
            'A': 'T',
            'T': 'A',
            'G': 'C',
            'C': 'G'
        }
        return [(base, complement[base]) for base in self.sequence]


class RNA:
    def __init__(self, sequence):
        self.sequence = sequence.upper()
        self._validate_sequence('AUGC')

    def _validate_sequence(self, allowed_bases):
        for base in self.sequence:
            if base not in allowed_bases:
                raise InvalidNucleotideError(f"Недопустимый нуклеотид '{base}' в последовательности РНК.")

    def to_list(self):
        return list(self.sequence)


class NucleotideHelper(DNA, RNA):
    def __init__(self, dna_sequence=None, rna_sequence=None):
        if dna_sequence:
            super(DNA, self).__init__(dna_sequence)
        if rna_sequence:
            super(RNA, self).__init__(rna_sequence)

    @staticmethod
    def to_set(nucleotide_list):
        return set(nucleotide_list)

    @staticmethod
    def rna_to_dna(rna_sequence):
        rna_to_dna_map = {
            'A': 'T',
            'U': 'A',
            'G': 'C',
            'C': 'G'
        }
        dna_first_strand = ''.join(rna_to_dna_map[base] for base in rna_sequence)
        complement = {
            'A': 'T',
            'T': 'A',
            'G': 'C',
            'C': 'G'
        }
        dna_second_strand = ''.join(complement[base] for base in dna_first_strand)
        return dna_first_strand, dna_second_strand

    @staticmethod
    def concatenate_rna(rna1, rna2):
        return rna1 + rna2

    @staticmethod
    def concatenate_dna(dna1, dna2):
        first_strand = dna1[0] + dna2[0]
        second_strand = dna1[1] + dna2[1]
        return [first_strand, second_strand]


class RNACrossOver(RNA):
    @staticmethod
    def crossover(rna1, rna2):
        result = []
        min_length = min(len(rna1), len(rna2))
        for i in range(min_length):
            result.append(random.choice([rna1[i], rna2[i]]))
        if len(rna1) > len(rna2):
            result.extend(rna1[min_length:])
        else:
            result.extend(rna2[min_length:])
        return ''.join(result)


class DNACrossOver(DNA):
    @staticmethod
    def crossover(dna1, dna2):
        first_strand1, second_strand1 = dna1
        first_strand2, second_strand2 = dna2

        # Перемножение первых цепочек
        crossed_first_strand = RNACrossOver.crossover(first_strand1, first_strand2)

        # Построение второй цепочки как комплементарной первой
        complement = {
            'A': 'T',
            'T': 'A',
            'G': 'C',
            'C': 'G'
        }
        crossed_second_strand = ''.join(complement[base] for base in crossed_first_strand)

        return [crossed_first_strand, crossed_second_strand]


class NucleotideComparator(DNA, RNA):
    @staticmethod
    def are_equal_dna_rna(dna, rna):
        # Преобразуем РНК в ДНК
        rna_to_dna_map = {
            'A': 'T',
            'U': 'A',
            'G': 'C',
            'C': 'G'
        }
        rna_dna_sequence = ''.join(rna_to_dna_map[base] for base in rna)

        # Сравниваем обе цепочки ДНК с преобразованной РНК
        return dna[0] == rna_dna_sequence or dna[1] == rna_dna_sequence

    @staticmethod
    def are_equal_concatenated_dna_rna(concatenated_dna, concatenated_rna):
        # Преобразуем склеенную РНК в ДНК
        rna_to_dna_map = {
            'A': 'T',
            'U': 'A',
            'G': 'C',
            'C': 'G'
        }
        concatenated_rna_dna_sequence = ''.join(rna_to_dna_map[base] for base in concatenated_rna)

        # Сравниваем обе цепочки склеенной ДНК с преобразованной склеенной РНК
        return concatenated_dna[0] == concatenated_rna_dna_sequence or concatenated_dna[
            1] == concatenated_rna_dna_sequence


class NucleotideApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Nucleotide App")

        self.dna_seq1_label = tk.Label(root, text="ДНК последовательность 1:")
        self.dna_seq1_label.grid(row=0, column=0)
        self.dna_seq1_entry = tk.Entry(root)
        self.dna_seq1_entry.grid(row=0, column=1)
        self.dna_seq1_entry.bind("<KeyRelease>", self.update_results)

        self.dna_seq2_label = tk.Label(root, text="ДНК последовательность 2:")
        self.dna_seq2_label.grid(row=1, column=0)
        self.dna_seq2_entry = tk.Entry(root)
        self.dna_seq2_entry.grid(row=1, column=1)
        self.dna_seq2_entry.bind("<KeyRelease>", self.update_results)

        self.rna_seq1_label = tk.Label(root, text="РНК последовательность 1:")
        self.rna_seq1_label.grid(row=2, column=0)
        self.rna_seq1_entry = tk.Entry(root)
        self.rna_seq1_entry.grid(row=2, column=1)
        self.rna_seq1_entry.bind("<KeyRelease>", self.update_results)

        self.rna_seq2_label = tk.Label(root, text="РНК последовательность 2:")
        self.rna_seq2_label.grid(row=3, column=0)
        self.rna_seq2_entry = tk.Entry(root)
        self.rna_seq2_entry.grid(row=3, column=1)
        self.rna_seq2_entry.bind("<KeyRelease>", self.update_results)

        self.dna_concatenate_label = tk.Label(root, text="Склеенная ДНК:")
        self.dna_concatenate_label.grid(row=4, column=0)
        self.dna_concatenate_result = tk.Label(root, text="")
        self.dna_concatenate_result.grid(row=4, column=1)

        self.rna_concatenate_label = tk.Label(root, text="Склеенная РНК:")
        self.rna_concatenate_label.grid(row=5, column=0)
        self.rna_concatenate_result = tk.Label(root, text="")
        self.rna_concatenate_result.grid(row=5, column=1)

        self.dna_crossover_label = tk.Label(root, text="Перемноженная ДНК:")
        self.dna_crossover_label.grid(row=6, column=0)
        self.dna_crossover_result = tk.Label(root, text="")
        self.dna_crossover_result.grid(row=6, column=1)

        self.rna_crossover_label = tk.Label(root, text="Перемноженная РНК:")
        self.rna_crossover_label.grid(row=7, column=0)
        self.rna_crossover_result = tk.Label(root, text="")
        self.rna_crossover_result.grid(row=7, column=1)

        self.dna_rna_equal_label = tk.Label(root, text="Равны ли ДНК и РНК:")
        self.dna_rna_equal_label.grid(row=8, column=0)
        self.dna_rna_equal_result = tk.Label(root, text="")
        self.dna_rna_equal_result.grid(row=8, column=1)

        self.concatenated_dna_rna_equal_label = tk.Label(root, text="Равны ли склеенные ДНК и РНК:")
        self.concatenated_dna_rna_equal_label.grid(row=9, column=0)
        self.concatenated_dna_rna_equal_result = tk.Label(root, text="")
        self.concatenated_dna_rna_equal_result.grid(row=9, column=1)

        self.crossed_dna_rna_equal_label = tk.Label(root, text="Равны ли перемноженные ДНК и РНК:")
        self.crossed_dna_rna_equal_label.grid(row=10, column=0)
        self.crossed_dna_rna_equal_result = tk.Label(root, text="")
        self.crossed_dna_rna_equal_result.grid(row=10, column=1)

    def update_results(self, event=None):
        try:
            dna1_seq = self.dna_seq1_entry.get()
            dna2_seq = self.dna_seq2_entry.get()
            rna1_seq = self.rna_seq1_entry.get()
            rna2_seq = self.rna_seq2_entry.get()

            if dna1_seq and dna2_seq:
                dna1 = DNA(dna1_seq)
                dna2 = DNA(dna2_seq)
                concatenated_dna = NucleotideHelper.concatenate_dna([dna1.sequence, dna1.sequence],
                                                                    [dna2.sequence, dna2.sequence])
                self.dna_concatenate_result.config(text=f"{concatenated_dna}")
                print(f"Склеенная ДНК: {concatenated_dna}")

                crossed_dna = DNACrossOver.crossover([dna1.sequence, dna1.sequence], [dna2.sequence, dna2.sequence])
                self.dna_crossover_result.config(text=f"{crossed_dna}")
                print(f"Перемноженная ДНК: {crossed_dna}")

            if rna1_seq and rna2_seq:
                rna1 = RNA(rna1_seq)
                rna2 = RNA(rna2_seq)
                concatenated_rna = NucleotideHelper.concatenate_rna(rna1.sequence, rna2.sequence)
                self.rna_concatenate_result.config(text=f"{concatenated_rna}")
                print(f"Склеенная РНК: {concatenated_rna}")

                crossed_rna = RNACrossOver.crossover(rna1.sequence, rna2.sequence)
                self.rna_crossover_result.config(text=f"{crossed_rna}")
                print(f"Перемноженная РНК: {crossed_rna}")

            if dna1_seq and rna1_seq:
                dna1 = DNA(dna1_seq)
                rna1 = RNA(rna1_seq)
                are_equal_dna_rna = NucleotideComparator.are_equal_dna_rna([dna1.sequence, dna1.sequence],
                                                                           rna1.sequence)
                self.dna_rna_equal_result.config(text=f"{are_equal_dna_rna}")
                print(f"Равны ли ДНК и РНК: {are_equal_dna_rna}")

            if dna1_seq and dna2_seq and rna1_seq and rna2_seq:
                concatenated_dna = NucleotideHelper.concatenate_dna([dna1.sequence, dna1.sequence],
                                                                    [dna2.sequence, dna2.sequence])
                concatenated_rna = NucleotideHelper.concatenate_rna(rna1.sequence, rna2.sequence)
                are_equal_concatenated_dna_rna = NucleotideComparator.are_equal_concatenated_dna_rna(concatenated_dna,
                                                                                                     concatenated_rna)
                self.concatenated_dna_rna_equal_result.config(text=f"{are_equal_concatenated_dna_rna}")
                print(f"Равны ли склеенные ДНК и РНК: {are_equal_concatenated_dna_rna}")

                crossed_dna = DNACrossOver.crossover([dna1.sequence, dna1.sequence], [dna2.sequence, dna2.sequence])
                crossed_rna = RNACrossOver.crossover(rna1.sequence, rna2.sequence)
                are_equal_crossed_dna_rna = NucleotideComparator.are_equal_dna_rna(crossed_dna, crossed_rna)
                self.crossed_dna_rna_equal_result.config(text=f"{are_equal_crossed_dna_rna}")
                print(f"Равны ли перемноженные ДНК и РНК: {are_equal_crossed_dna_rna}")

        except InvalidNucleotideError as e:
            messagebox.showerror("Ошибка", str(e))
            print(f"Ошибка: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = NucleotideApp(root)
    root.mainloop()