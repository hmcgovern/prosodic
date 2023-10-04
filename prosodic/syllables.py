from .imports import *



class Syllable(entity):
    prefix='syll'
    child_type = 'Phoneme'
    
    @profile
    def __init__(self, txt:str, ipa=None, parent=None, children=[], **kwargs):
        from .phonemes import Phoneme
        from gruut_ipa import Pronunciation
        assert ipa or children
        if ipa and not children:
            sipa=''.join(x for x in ipa if x.isalpha())
            pron = Pronunciation.from_string(sipa)
            phones = [p.text for p in pron if p.text]
            children = [Phoneme(phon) for phon in phones]
        super().__init__(txt=txt, ipa=ipa, children=children, parent=parent, **kwargs)
    
    @cached_property
    def stress(self): return get_stress(self.ipa)
    
    @cached_property
    def attrs(self):
        return {
            **self._attrs,
            'num':self.num,
            'txt':self.txt, 
            'is_stressed':self.is_stressed, 
            'is_heavy':self.is_heavy, 
            'is_strong':self.is_strong, 
            'is_weak':self.is_weak,
        }

    
    @cached_property
    def has_consonant_ending(self):
        return self.children[-1].cons>0
    
    @cached_property
    def num_vowels(self):
        return sum(1 for phon in self.children if phon.cons<=0)
    
    @cached_property
    def has_dipthong(self):
        return self.num_vowels>1
    
    @cached_property
    def is_stressed(self):
        return self.stress in {'S','P'}
    
    @cached_property
    def is_heavy(self):
        return bool(self.has_consonant_ending or self.has_dipthong)
    
    
    @cached_property
    def is_strong(self):
        if not len(self.parent.children)>1: return None
        if not self.is_stressed: return False
        if self.prev and not self.prev.is_stressed: return True
        if self.next and not self.next.is_stressed: return True

    @cached_property
    def is_weak(self):
        if not len(self.parent.children)>1: return None
        if self.is_stressed: return False
        if self.prev and self.prev.is_stressed: return True
        if self.next and self.next.is_stressed: return True