"""
Command-line interface for SvaraScala.
"""

import argparse
import sys
from .western import WesternMusic
from .modes import WesternModes
from .indian import IndianMusic
from .navarasa import NavarasaMap


def format_freq(freq):
    """Format frequency to 2 decimal places"""
    return f"{freq:.2f} Hz"

def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(title.center(60))
    print("=" * 60)

def western_note_info(args):
    """Display information about a Western note"""
    wm = WesternMusic(reference_a4=args.reference)
    
    try:
        freq = wm.get_frequency(args.note, args.octave)
        print(f"\nNote: {args.note}{args.octave}")
        print(f"Frequency: {format_freq(freq)}")
        
        # Show related harmonic notes
        print("\nHarmonic relationships:")
        for other_note in wm.notes:
            for other_octave in range(args.octave - 1, args.octave + 2):
                if other_note == args.note and other_octave == args.octave:
                    continue
                is_harmonic, relation = wm.are_harmonic(args.note, args.octave, other_note, other_octave)
                if is_harmonic:
                    other_freq = wm.get_frequency(other_note, other_octave)
                    print(f"  {other_note}{other_octave} ({format_freq(other_freq)}) - {relation}")
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0

def western_scale_info(args):
    """Display information about a Western scale"""
    wm = WesternMusic(reference_a4=args.reference)
    
    try:
        scale = wm.get_scale(args.root, args.octave, args.scale_type)
        
        print(f"\nScale: {args.root} {args.scale_type}, Octave: {args.octave}")
        print("-" * 40)
        print(f"{'Note':<10} {'Frequency':<15}")
        print("-" * 40)
        
        for note, freq in scale.items():
            print(f"{note:<10} {format_freq(freq)}")
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0

def western_mode_info(args):
    """Display information about a Western mode"""
    wm = WesternModes(reference_a4=args.reference)
    
    try:
        # Get mode information
        mode_info = wm.get_mode_info(args.mode)
        
        print_header(f"{args.mode} Mode")
        
        print(f"\nPrimary emotion: {mode_info['primary']}")
        print(f"Character: {mode_info['character']}")
        print(f"Associated moods: {', '.join(mode_info['moods'])}")
        print(f"Western parallel: {mode_info['western_parallel']}")
        print(f"Energy level: {mode_info['energy_level']}/10")
        print(f"Emotional intensity: {mode_info['emotional_intensity']}/10")
        
        # Show historical usage if requested
        if args.with_history:
            history = wm.get_historical_usage(args.mode)
            print("\nHistorical Usage:")
            print(f"Eras: {', '.join(history['eras'])}")
            print(f"Prominence: {history['prominence']}")
            print(f"Typical contexts: {', '.join(history['contexts'])}")
        
        # Show frequencies if octave is provided
        if args.root and args.octave:
            frequencies = wm.get_mode_frequencies(args.mode, args.root, args.octave)
            
            print(f"\nScale: {args.root} {args.mode}, Octave: {args.octave}")
            print("-" * 40)
            print(f"{'Note':<10} {'Frequency':<15}")
            print("-" * 40)
            
            for note, freq in frequencies.items():
                print(f"{note:<10} {format_freq(freq)}")
        
        # Show chord progressions if requested
        if args.with_progressions:
            progressions = wm.get_common_chord_progressions(args.mode)
            print("\nCommon Chord Progressions:")
            for progression in progressions:
                print(f"  {progression}")
        
        # Show compatible modes
        if args.with_transitions:
            compatible_modes = wm.get_compatible_modes(args.mode)
            
            print("\nCompatible Mode Transitions:")
            for target_mode, details in compatible_modes.items():
                print(f"\n→ {target_mode} ({details['primary_emotion']})")
                print(f"  Character: {details['character']}")
                print(f"  {details['energy_transition']} ({details['energy_difference']} change)")
                print(f"  Recommended instruments: {', '.join(details['recommended_instruments'][:3])}")
        
        # Show Indian connections if requested
        if args.with_indian:
            from .navarasa import NavarasaMap
            nv = NavarasaMap(reference_sa=220.0)
            
            # Get corresponding rasas
            rasas = wm.get_corresponding_rasa(args.mode)
            
            print("\nCorresponding Indian Rasas:")
            for rasa in rasas:
                try:
                    rasa_info = nv.get_rasa_info(rasa)
                    print(f"  {rasa} - {rasa_info['english']} (Mood: {rasa_info['mood']})")
                except ValueError:
                    print(f"  {rasa} (detailed information not available)")
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0

def indian_swara_info(args):
    """Display information about an Indian swara"""
    im = IndianMusic(reference_sa=args.reference)
    
    try:
        variant = args.variant if args.variant else "shuddha"
        freq = im.get_swara_frequency(args.swara, variant)
        
        print(f"\nSwara: {args.swara} {variant}")
        print(f"Frequency: {format_freq(freq)}")
        
        # Show ratio from Sa
        ratio = freq / im.reference_sa
        print(f"Ratio from Sa: {ratio:.4f}")
        
        # Show corresponding shruti
        if args.swara == "Sa" or args.swara == "Pa":
            shruti_num = im.swara_to_shruti[args.swara]
        else:
            shruti_num = im.swara_to_shruti[args.swara][variant]
        
        print(f"Corresponding Shruti: {shruti_num}")
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0

def indian_raga_info(args):
    """Display information about an Indian raga"""
    im = IndianMusic(reference_sa=args.reference)
    
    try:
        frequencies = im.calculate_raga_frequencies(args.raga)
        
        print(f"\nRaga: {args.raga}, Sa: {format_freq(args.reference)}")
        print("-" * 40)
        print(f"{'Swara':<15} {'Frequency':<15} {'Ratio to Sa':<15}")
        print("-" * 40)
        
        for swara, freq in frequencies.items():
            ratio = freq / im.reference_sa
            print(f"{swara:<15} {format_freq(freq):<15} {ratio:.4f}")
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0

def western_camelot_info(args):
    """Display information about a key using Camelot Wheel notation"""
    wm = WesternMusic(reference_a4=args.reference)
    
    try:
        # If camelot notation is provided, convert to key
        if args.camelot:
            key, scale_type = wm.get_key_from_camelot(args.camelot)
            print(f"\nCamelot Notation: {args.camelot}")
            print(f"Corresponding Key: {key} {scale_type}")
        else:
            # Otherwise, use the provided key and scale type
            key = args.key
            scale_type = args.scale_type
            camelot = wm.get_camelot_notation(key, scale_type)
            print(f"\nKey: {key} {scale_type}")
            print(f"Camelot Notation: {camelot}")
        
        # Get compatible keys regardless of input type
        if args.camelot:
            camelot_notation = args.camelot
        else:
            camelot_notation = wm.get_camelot_notation(key, scale_type)
        
        compatible_keys = wm.get_compatible_keys(camelot_notation)
        
        print("\nHarmonically Compatible Keys:")
        print("-" * 60)
        print(f"{'Camelot':<8} {'Key':<15} {'Relationship':<30}")
        print("-" * 60)
        
        for notation, description in compatible_keys.items():
            related_key, related_scale = wm.get_key_from_camelot(notation)
            print(f"{notation:<8} {related_key} {related_scale:<10} {description}")
        
        # If requested, also show the scale frequencies
        if args.with_frequencies:
            if args.octave is None:
                print("\nNote: Specify --octave to see frequencies")
            else:
                scale_with_camelot = wm.get_scale_with_camelot(key, args.octave, scale_type)
                print(f"\nScale: {key} {scale_type}, Octave: {args.octave}")
                print("-" * 40)
                print(f"{'Note':<10} {'Frequency':<15}")
                print("-" * 40)
                
                for note, freq in scale_with_camelot['frequencies'].items():
                    print(f"{note:<10} {format_freq(freq)}")
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0

def navarasa_info(args):
    """Display information about using the Navarasa wheel."""
    from .navarasa import NavarasaMap
    
    nw = NavarasaMap(reference_sa=args.reference)
    
    # If a specific rasa is requested
    if args.rasa:
        try:
            # Get info about the rasa
            rasa_info = nw.get_rasa_info(args.rasa)
            
            print(f"\nRasa: {args.rasa}")
            print(f"English: {rasa_info['english']}")
            print(f"Mood: {rasa_info['mood']}")
            print(f"Time: {rasa_info['time']}")
            print(f"Color: {rasa_info['color']}")
            print(f"Energy Level: {nw.energy_levels[args.rasa]}/10")
            
            # Get ragas for this rasa
            ragas = nw.get_raga_by_rasa(args.rasa)
            print("\nAssociated Ragas:")
            for raga in ragas:
                print(f"  {raga}")
            
            # Show compatible transitions
            if args.with_transitions:
                transitions = nw.get_compatible_rasas(args.rasa)
                print("\nCompatible Emotional Transitions:")
                for target_rasa, details in transitions.items():
                    print(f"\n→ {target_rasa} ({details['description']})")
                    print(f"  {details['transition_type']} ({details['energy_difference']} change)")
                    print("  Recommended ragas:")
                    for raga in details['recommended_ragas'][:3]:  # Show just top 3
                        print(f"  - {raga}")
        
        except ValueError as e:
            print(f"Error: {str(e)}")
            return 1
    
    # If a specific raga is requested
    elif args.raga:
        try:
            print(f"\nRaga: {args.raga}")
            
            # Get rasas associated with this raga
            rasas = nw.get_rasa_from_raga(args.raga)
            
            if not rasas:
                print("This raga is not classified in the Navarasa system.")
            else:
                print("\nAssociated Rasas:")
                for rasa in rasas:
                    rasa_info = nw.get_rasa_info(rasa)
                    print(f"  {rasa} - {rasa_info['english']} (Mood: {rasa_info['mood']})")
                
                # Get frequencies
                if args.with_frequencies:
                    freqs = nw.get_raga_frequencies(args.raga)
                    print("\nFrequencies:")
                    for swara, freq in freqs.items():
                        print(f"  {swara}: {freq:.2f} Hz")
                
                # Get Western equivalents
                if args.with_western:
                    western_equiv = nw.get_western_equivalent(args.raga)
                    
                    if "message" in western_equiv:
                        print(f"\nWestern equivalent: {western_equiv['message']}")
                    else:
                        print(f"\nWestern equivalent: {western_equiv['scale_type']}")
                        print(f"Suggested key: {western_equiv['suggested_key']}")
                        print(f"Thaat: {western_equiv['thaat']}")
                        
                        # Display Camelot notation for DJs
                        if western_equiv['camelot_notation']:
                            print(f"\nDJ Mixing Information:")
                            print(f"  Camelot notation: {western_equiv['camelot_notation']}")
                            
                            # Show compatible keys in Camelot wheel
                            print("  Compatible DJ keys (Camelot wheel):")
                            for camelot, key in western_equiv['compatible_camelot_keys'].items():
                                print(f"    {camelot}: {key}")
                        
                        print(f"\nWestern correlations: {', '.join(western_equiv['western_correlations'])}")

        except Exception as e:
            print(f"Error: {str(e)}")
            return 1
    
    # If a transition path is requested
    elif args.from_rasa and args.to_rasa:
        try:
            print(f"\nFinding transition path from {args.from_rasa} to {args.to_rasa}")
            
            # Get path
            path = nw.suggest_transition_path(args.from_rasa, args.to_rasa, args.max_steps)
            
            if path:
                print(f"\nRecommended path: {' → '.join(path)}")
                
                print("\nDetails for each stage:")
                for i, rasa in enumerate(path):
                    rasa_info = nw.get_rasa_info(rasa)
                    print(f"\nStage {i+1}: {rasa} ({rasa_info['english']})")
                    print(f"Mood: {rasa_info['mood']}, Energy level: {nw.energy_levels[rasa]}/10")
                    
                    # Show recommended ragas
                    ragas = nw.get_raga_by_rasa(rasa)
                    print("Recommended ragas:")
                    for raga in ragas[:3]:  # Show top 3
                        print(f"  - {raga}")
            else:
                print(f"No path found from {args.from_rasa} to {args.to_rasa} within {args.max_steps} steps.")
        
        except ValueError as e:
            print(f"Error: {str(e)}")
            return 1
    
    # If no specific parameters, show general information
    else:
        print("\nNavarasa (Nine Sentiments) in Indian Classical Music")
        print("-" * 50)
        print("The nine emotional states (rasas) and their characteristics:")
        
        for rasa, info in nw.rasas.items():
            print(f"\n{rasa} - {info['english']}")
            print(f"  Mood: {info['mood']}")
            print(f"  Energy Level: {nw.energy_levels[rasa]}/10")
    
    return 0

def cross_cultural_comparison(args):
    """Display a comparison between Western modes and Indian ragas."""
    from .modes import WesternModes
    from .navarasa import NavarasaMap
    
    wm = WesternModes(reference_a4=args.reference)
    nv = NavarasaMap(reference_sa=args.reference_sa)
    
    try:
        if args.mode and args.raga:
            # Compare specific mode to specific raga
            print_header(f"Comparison: {args.mode} Mode vs {args.raga} Raga")
            
            # Get mode info
            mode_info = wm.get_mode_info(args.mode)
            
            # Get frequencies if root and octave provided
            mode_freqs = {}
            if args.root and args.octave:
                mode_freqs = wm.get_mode_frequencies(args.mode, args.root, args.octave)
            
            # Get raga info and frequencies
            raga_freqs = nv.get_raga_frequencies(args.raga)
            rasas = nv.get_rasa_from_raga(args.raga)
            
            # Display comparison
            print(f"\nWestern Mode: {args.mode}")
            print(f"Primary emotion: {mode_info['primary']}")
            print(f"Character: {mode_info['character']}")
            
            print(f"\nIndian Raga: {args.raga}")
            print("Associated Rasas:")
            for rasa in rasas:
                rasa_info = nv.get_rasa_info(rasa)
                print(f"  {rasa} - {rasa_info['english']} (Mood: {rasa_info['mood']})")
            
            # Show cultural correlations
            mode_rasas = wm.get_corresponding_rasa(args.mode)
            overlap = set(rasas).intersection(set(mode_rasas))
            
            print("\nCultural Correlation:")
            if overlap:
                print(f"Strong emotional correlation through shared rasas: {', '.join(overlap)}")
            else:
                print("No direct rasa correlation, but similar emotional qualities may exist")
            
            # Show frequencies if requested
            if args.with_frequencies and args.root and args.octave:
                print("\nFrequency Comparison:")
                print("-" * 60)
                print(f"{'Western Note':<15} {'Frequency':<15} | {'Indian Swara':<15} {'Frequency':<15}")
                print("-" * 60)
                
                # Get at most 7 notes from each to compare
                mode_notes = list(mode_freqs.items())[:7]
                raga_notes = list(raga_freqs.items())[:7]
                
                # Determine the maximum length to iterate
                max_length = max(len(mode_notes), len(raga_notes))
                
                for i in range(max_length):
                    western_note = mode_notes[i][0] if i < len(mode_notes) else ""
                    western_freq = format_freq(mode_notes[i][1]) if i < len(mode_notes) else ""
                    
                    indian_note = raga_notes[i][0] if i < len(raga_notes) else ""
                    indian_freq = format_freq(raga_notes[i][1]) if i < len(raga_notes) else ""
                    
                    print(f"{western_note:<15} {western_freq:<15} | {indian_note:<15} {indian_freq:<15}")
        
        elif args.mode:
            # Show mode info with raga recommendations
            comparison = wm.compare_mode_to_raga(args.mode, args.root if args.root else "C", 
                                               args.octave if args.octave else 4, nv)
            
            print_header(f"{args.mode} Mode - Indian Music Equivalents")
            
            print(f"\nWestern Mode: {args.mode}")
            print(f"Emotional character: {comparison['emotional_character']}")
            
            print("\nCorresponding Indian Rasas:")
            for rasa in comparison['corresponding_rasas']:
                try:
                    rasa_info = nv.get_rasa_info(rasa)
                    print(f"  {rasa} - {rasa_info['english']} (Mood: {rasa_info['mood']})")
                except ValueError:
                    print(f"  {rasa}")
            
            if 'related_ragas' in comparison and comparison['related_ragas']:
                print("\nRecommended Indian Ragas:")
                for raga in comparison['related_ragas'][:5]:  # Show top 5
                    print(f"  {raga}")
            
            # Show frequencies if requested
            if args.with_frequencies:
                if args.root and args.octave:
                    frequencies = wm.get_mode_frequencies(args.mode, args.root, args.octave)
                    
                    print(f"\nMode Scale: {args.root} {args.mode}, Octave: {args.octave}")
                    print("-" * 40)
                    print(f"{'Note':<10} {'Frequency':<15}")
                    print("-" * 40)
                    
                    for note, freq in frequencies.items():
                        print(f"{note:<10} {format_freq(freq)}")
                else:
                    print("\nNote: Specify --root and --octave to see frequencies")
        
        elif args.raga:
            # Show raga info with mode recommendations
            western_equiv = nv.get_western_equivalent(args.raga)
            
            print_header(f"{args.raga} Raga - Western Music Equivalents")
            
            print(f"\nIndian Raga: {args.raga}")
            
            # Get rasas
            rasas = nv.get_rasa_from_raga(args.raga)
            print("\nAssociated Rasas:")
            for rasa in rasas:
                rasa_info = nv.get_rasa_info(rasa)
                print(f"  {rasa} - {rasa_info['english']} (Mood: {rasa_info['mood']})")
            
            # Show Western equivalents
            print("\nWestern Equivalent:")
            if "message" in western_equiv:
                print(f"  {western_equiv['message']}")
            else:
                print(f"  Scale type: {western_equiv['scale_type']}")
                print(f"  Suggested key: {western_equiv['suggested_key']}")
                
                # Suggest modes based on the rasas
                suggested_modes = []
                for rasa in rasas:
                    for mode, corresponding_rasas in wm.mode_to_rasa_map.items():
                        if rasa in corresponding_rasas and mode not in suggested_modes:
                            suggested_modes.append(mode)
                
                if suggested_modes:
                    print("\nRecommended Western Modes:")
                    for mode in suggested_modes:
                        mode_info = wm.get_mode_info(mode)
                        print(f"  {mode} - {mode_info['primary']} ({mode_info['character']})")
            
            # Show frequencies
            if args.with_frequencies:
                frequencies = nv.get_raga_frequencies(args.raga)
                
                print(f"\nRaga: {args.raga}, Sa: {format_freq(args.reference_sa)}")
                print("-" * 40)
                print(f"{'Swara':<15} {'Frequency':<15}")
                print("-" * 40)
                
                for swara, freq in frequencies.items():
                    print(f"{swara:<15} {format_freq(freq)}")
        
        else:
            # Show general comparison information
            print_header("Cross-Cultural Musical Emotion Comparison")
            
            print("\nWestern Modes and their emotional characteristics:")
            for mode, info in wm.modal_emotions.items():
                print(f"\n{mode}:")
                print(f"  Primary emotion: {info['primary']}")
                print(f"  Character: {info['character']}")
                
                # Show corresponding rasas
                corresponding_rasas = wm.get_corresponding_rasa(mode)
                if corresponding_rasas:
                    print(f"  Corresponding Indian rasas: {', '.join(corresponding_rasas)}")
            
            print("\n" + "-" * 60)
            print("Indian Rasas and their emotional characteristics:")
            
            for rasa, info in nv.rasas.items():
                print(f"\n{rasa}:")
                print(f"  English: {info['english']}")
                print(f"  Mood: {info['mood']}")
                
                # Find modes that map to this rasa
                corresponding_modes = []
                for mode, rasas in wm.mode_to_rasa_map.items():
                    if rasa in rasas:
                        corresponding_modes.append(mode)
                
                if corresponding_modes:
                    print(f"  Corresponding Western modes: {', '.join(corresponding_modes)}")
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0

def main():
    """Main entry point for the command line interface"""
    parser = argparse.ArgumentParser(description="SvaraScala - Musical frequency calculations")
    subparsers = parser.add_subparsers(dest="command", help="Command")
    
    # Western note parser
    western_note_parser = subparsers.add_parser("western-note", help="Get information about a Western note")
    western_note_parser.add_argument("note", help="Note name (e.g., C, F#)")
    western_note_parser.add_argument("octave", type=int, help="Octave number")
    western_note_parser.add_argument("--reference", type=float, default=440.0, help="Reference frequency for A4 (default: 440 Hz)")
    
    # Western scale parser
    western_scale_parser = subparsers.add_parser("western-scale", help="Get information about a Western scale")
    western_scale_parser.add_argument("root", help="Root note (e.g., C, F#)")
    western_scale_parser.add_argument("octave", type=int, help="Octave number")
    western_scale_parser.add_argument("--scale-type", default="major", help="Scale type (e.g., major, minor, blues)")
    western_scale_parser.add_argument("--reference", type=float, default=440.0, help="Reference frequency for A4 (default: 440 Hz)")
    
    # Western mode parser
    western_mode_parser = subparsers.add_parser("western-mode", help="Get information about a Western mode")
    western_mode_parser.add_argument("mode", help="Mode name (e.g., Ionian, Dorian, Phrygian)")
    western_mode_parser.add_argument("--root", help="Root note for frequency calculations (e.g., C, F#)")
    western_mode_parser.add_argument("--octave", type=int, help="Octave number for root note")
    western_mode_parser.add_argument("--with-history", action="store_true", help="Show historical usage information")
    western_mode_parser.add_argument("--with-transitions", action="store_true", help="Show compatible mode transitions")
    western_mode_parser.add_argument("--with-progressions", action="store_true", help="Show common chord progressions")
    western_mode_parser.add_argument("--with-indian", action="store_true", help="Show connections to Indian music")
    western_mode_parser.add_argument("--reference", type=float, default=440.0, help="Reference frequency for A4 (default: 440 Hz)")
    
    # Camelot Wheel parser
    camelot_parser = subparsers.add_parser("camelot", help="Get information using Camelot Wheel notation")
    camelot_group = camelot_parser.add_mutually_exclusive_group(required=True)
    camelot_group.add_argument("--camelot", help="Camelot notation (e.g., 8B, 5A)")
    camelot_group.add_argument("--key", help="Key name (e.g., C, F#)")
    camelot_parser.add_argument("--scale-type", default="major", choices=["major", "minor"], 
                            help="Scale type (required if using --key)")
    camelot_parser.add_argument("--octave", type=int, help="Octave number (for frequency calculations)")
    camelot_parser.add_argument("--with-frequencies", action="store_true", 
                            help="Show frequencies (requires --octave)")
    camelot_parser.add_argument("--reference", type=float, default=440.0, 
                            help="Reference frequency for A4 (default: 440 Hz)")

    # Indian swara parser
    indian_swara_parser = subparsers.add_parser("indian-swara", help="Get information about an Indian swara")
    indian_swara_parser.add_argument("swara", help="Swara name (e.g., Sa, Re, Ga)")
    indian_swara_parser.add_argument("--variant", help="Variant (e.g., komal, shuddha, tivra)")
    indian_swara_parser.add_argument("--reference", type=float, default=220.0, help="Reference frequency for Sa (default: 220 Hz)")
    
    # Indian raga parser
    indian_raga_parser = subparsers.add_parser("indian-raga", help="Get information about an Indian raga")
    indian_raga_parser.add_argument("raga", help="Raga name (e.g., Yaman, Bhairav)")
    indian_raga_parser.add_argument("--reference", type=float, default=220.0, help="Reference frequency for Sa (default: 220 Hz)")

    # Navarasa parser
    navarasa_parser = subparsers.add_parser("navarasa", help="Get information using the Navarasa (nine sentiments) wheel")
    navarasa_group = navarasa_parser.add_mutually_exclusive_group()
    navarasa_group.add_argument("--rasa", help="Get information about a specific rasa (e.g., Sringara, Karuna)")
    navarasa_group.add_argument("--raga", help="Get information about a raga in the Navarasa system")
    navarasa_parser.add_argument("--with-frequencies", action="store_true", help="Show frequencies (for raga queries)")
    navarasa_parser.add_argument("--with-western", action="store_true", help="Show Western equivalents (for raga queries)")
    navarasa_parser.add_argument("--with-transitions", action="store_true", help="Show transition information (for rasa queries)")
    navarasa_parser.add_argument("--from-rasa", help="Starting rasa for transition path")
    navarasa_parser.add_argument("--to-rasa", help="Target rasa for transition path")
    navarasa_parser.add_argument("--max-steps", type=int, default=3, help="Maximum steps in transition path")
    navarasa_parser.add_argument("--reference", type=float, default=220.0, help="Reference frequency for Sa (default: 220 Hz)")

    # Cross-cultural comparison parser
    cross_cultural_parser = subparsers.add_parser("compare", help="Compare Western modes and Indian ragas")
    cross_cultural_group = cross_cultural_parser.add_mutually_exclusive_group()
    cross_cultural_group.add_argument("--mode", help="Western mode to compare (e.g., Dorian, Phrygian)")
    cross_cultural_group.add_argument("--raga", help="Indian raga to compare (e.g., Yaman, Bhairav)")
    cross_cultural_parser.add_argument("--root", help="Root note for Western mode (e.g., C, F#)")
    cross_cultural_parser.add_argument("--octave", type=int, help="Octave number for root note")
    cross_cultural_parser.add_argument("--with-frequencies", action="store_true", help="Show frequencies in comparison")
    cross_cultural_parser.add_argument("--reference", type=float, default=440.0, help="Reference frequency for A4 (default: 440 Hz)")
    cross_cultural_parser.add_argument("--reference-sa", type=float, default=220.0, help="Reference frequency for Sa (default: 220 Hz)")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return 0

    # Dispatch to the appropriate handler
    if args.command == "western-note":
        return western_note_info(args)
    elif args.command == "western-scale":
        return western_scale_info(args)
    elif args.command == "western-mode":
        return western_mode_info(args)
    elif args.command == "camelot":
        return western_camelot_info(args)
    elif args.command == "indian-swara":
        return indian_swara_info(args)
    elif args.command == "indian-raga":
        return indian_raga_info(args)
    elif args.command == "navarasa":
        return navarasa_info(args)
    elif args.command == "compare":
        return cross_cultural_comparison(args)

    return 0

if __name__ == "__main__":
    sys.exit(main())